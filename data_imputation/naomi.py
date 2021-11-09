import numpy as np 
import pandas as pd  
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from torch.autograd import Variable
import torch
import torch.utils
import torch.utils.data
from torch import nn

from tqdm import trange
import sys

class NAMOIimputation:
    def __init__(self, path, window_size = 50, use_gpu = torch.cuda.is_available()):
        self.path = path
        self.window_size = window_size
        self.df, self.data, self.scaler, self.data_batch = self.makeBatch()
        self.model = None
        self.use_gpu = use_gpu
        self.device = torch.device("cuda") if use_gpu else torch.device("cpu")
        self.result = None

    def makeBatch(self):
        df = pd.read_csv(self.path)
        min_max_scaler = MinMaxScaler()
        df = df[["time", "value"]]
        df["value"] = min_max_scaler.fit_transform(df["value"].values.reshape(-1,1))
        missing_list = df.isnull()["value"]
        data = df["value"].to_numpy()

        data_batch = []
        datas = []
        for index,val in enumerate(data):
            if missing_list[index]:
                datas=[]
                continue
            datas.append(val)         
            if len(datas)==self.window_size:
                data_batch.append(datas.copy())
                datas.pop(0)
        data_batch = np.array(data_batch)
        data_batch = data_batch.reshape(data_batch.shape[0], data_batch.shape[1], 1)
        return df,data, min_max_scaler, data_batch

    def predict_result(self):
        test = self.data.copy()
        missing_list = np.where(pd.isnull(test))

        test[np.isnan(test)] = 0
        
        test = test.reshape(len(self.data),1,1)
        test = Variable(torch.Tensor(test).to(self.device))

        has_value = Variable(torch.ones(test.shape[0], test.shape[1], 1))
        has_value[missing_list] = 0.0
        has_value = has_value.to(self.device)
        data_test = torch.cat([has_value, test], 2)

        data_list = []
        for j in range(len(self.data)):
            data_list.append(data_test[j:j+1])
        samples = self.model.sample(data_list,1)
        result = samples[:,0,0].cpu().detach().numpy()

        self.result = self.scaler.inverse_transform(result.reshape(-1,1))
        return self.result

    def plot(self):
        plt.figure(figsize=(20,5))
        plt.plot(self.data, label="real", zorder=10)
        plt.plot(self.result, label="predict")
        plt.legend()
        plt.show()


    def imputation(self, epoch = 250):
        pretrain_epochs = epoch
        clip = 10
        start_lr = 1e-3
        batch_size = 64

        np.random.seed(123)
        torch.manual_seed(123)
        if self.use_gpu:
            torch.cuda.manual_seed_all(123)

        params = {
            'task' : "--",
            'batch' : batch_size,
            'y_dim' : 1,
            'rnn_dim' : 50,
            'dec1_dim' : 30,
            'dec2_dim' : 30,
            'dec4_dim' : 30,
            'dec8_dim' : 30,
            'dec16_dim' : 30,
            'n_layers' : 2,
            'discrim_rnn_dim' : 128,
            'discrim_num_layers' : 1,
            'cuda' : self.use_gpu,
            'highest' : 8,
        }

        self.model = NAOMI(params).to(self.device)
        params['total_params'] = num_trainable_params(self.model)
        train_data = torch.Tensor(self.data_batch)

        lr = start_lr
        teacher_forcing = True
        with trange(pretrain_epochs, file=sys.stdout) as tr:
            for e in tr:
                
                epoch = e+1
                # control learning rate
                if epoch == pretrain_epochs // 2:
                    lr = lr / 10

                # train
                optimizer = torch.optim.Adam(
                    filter(lambda p: p.requires_grad, self.model.parameters()),
                    lr=lr)
                train_loss = self.run_epoch(True, self.model, train_data, clip, optimizer, batch_size = batch_size, teacher_forcing=teacher_forcing)
                # print("asf")
                
                tr.set_postfix(loss="{0:.3f}".format(train_loss))

        # filename = "model/model_pretrain.pth"
        # torch.save(policy_net.state_dict(), filename)

        self.result = self.predict_result()

        self.df["value"] = self.result 

        self.data = self.scaler.inverse_transform(self.data.reshape(-1,1))
        return self.df

    def run_epoch(self, train, model, exp_data, clip, optimizer=None, batch_size=64, num_missing=None, teacher_forcing=True):
        losses = []
        inds = np.random.permutation(exp_data.shape[0])
        
        i = 0
        while i + batch_size <= exp_data.shape[0]:
            ind = torch.from_numpy(inds[i:i+batch_size]).long()
            i += batch_size
            data = exp_data[ind]
        
            
            data = data.to(self.device)

            # change (batch, time, x) to (time, batch, x)
            data = Variable(data.transpose(0, 1))
            ground_truth = data.clone()
            if num_missing is None:
                #num_missing = np.random.randint(data.shape[0] * 18 // 20, data.shape[0])
                num_missing = np.random.randint(data.shape[0] * 4 // 5, data.shape[0])
                #num_missing = 40
            missing_list = torch.from_numpy(np.random.choice(np.arange(1, data.shape[0]), num_missing, replace=False)).long()
            data[missing_list] = 0.0
            has_value = Variable(torch.ones(data.shape[0], data.shape[1], 1))
            has_value = has_value.to(self.device)
            has_value[missing_list] = 0.0

            data = torch.cat([has_value, data], 2)
            seq_len = data.shape[0]


            if teacher_forcing:
                batch_loss = model(data, ground_truth)
            else:
                data_list = []
                for j in range(seq_len):
                    data_list.append(data[j:j+1])
                samples = model.sample(data_list)
                batch_loss = torch.mean((ground_truth - samples).pow(2))

            if train:
                optimizer.zero_grad()
                total_loss = batch_loss
                total_loss.backward()
                nn.utils.clip_grad_norm_(model.parameters(), clip)
                optimizer.step()
            
            losses.append(batch_loss.data.cpu().numpy())

        return np.mean(losses)


class NAOMI(nn.Module):
    def __init__(self, params):
        super(NAOMI, self).__init__()

        self.params = params
        self.task = params['task']
        self.stochastic = (self.task == 'basketball')
        self.y_dim = params['y_dim']
        self.rnn_dim = params['rnn_dim']
        self.dims = {}
        self.n_layers = params['n_layers']
        self.networks = {}
        self.highest = params['highest']
        self.batch_size = params['batch']

        self.gru = nn.GRU(self.y_dim, self.rnn_dim, self.n_layers)
        self.back_gru = nn.GRU(self.y_dim + 1, self.rnn_dim, self.n_layers)
        
        step = 1
        while step <= self.highest:
            l = str(step)
            self.dims[l] = params['dec' + l + '_dim']
            dim = self.dims[l]
            
            curr_level = {}
            curr_level['dec'] = nn.Sequential(
                nn.Linear(2 * self.rnn_dim, dim),
                nn.ReLU())
            curr_level['mean'] = nn.Linear(dim, self.y_dim)
            if self.stochastic:
                curr_level['std'] = nn.Sequential(
                    nn.Linear(dim, self.y_dim),
                    nn.Softplus())
            curr_level = nn.ModuleDict(curr_level)

            self.networks[l] = curr_level
            
            step = step * 2

        self.networks = nn.ModuleDict(self.networks)

    def forward(self, data, ground_truth):
        # data: seq_length * batch * 11
        # ground_truth: seq_length * batch * 10
        h = Variable(torch.zeros(self.n_layers, self.batch_size, self.rnn_dim))
        h_back = Variable(torch.zeros(self.n_layers, self.batch_size, self.rnn_dim))
        if self.params['cuda']:
            h, h_back = h.cuda(), h_back.cuda()
        
        loss = 0.0
        h_back_dict = {}
        count = 0
        
        for t in range(data.shape[0] - 1, 0, -1):
            h_back_dict[t+1] = h_back
            state_t = data[t]
            _, h_back = self.back_gru(state_t.unsqueeze(0), h_back)
            
        for t in range(data.shape[0]):
            state_t = ground_truth[t]
            _, h = self.gru(state_t.unsqueeze(0), h)
            count += 1
            for l, dim in self.dims.items():
                step_size = int(l)
                curr_level = self.networks[str(step_size)] 
                if t + 2 * step_size <= data.shape[0]:
                    next_t = ground_truth[t+step_size]
                    h_back = h_back_dict[t+2*step_size]
                    
                    dec_t = curr_level['dec'](torch.cat([h[-1], h_back[-1]], 1))
                    dec_mean_t = curr_level['mean'](dec_t)
                    
                    if self.stochastic:
                        dec_std_t = curr_level['std'](dec_t)
                        loss += nll_gauss(dec_mean_t, dec_std_t, next_t)
                    else:
                        loss += torch.sum((dec_mean_t - next_t).pow(2))

        return loss / count / data.shape[1]

    def sample(self, data_list, batch_size = None):
        if not batch_size:
            batch_size = self.batch_size
        # data_list: seq_length * (1 * batch * 11)
        ret = []
        seq_len = len(data_list)
        h = Variable(torch.zeros(self.params['n_layers'], batch_size, self.rnn_dim))
        if self.params['cuda']:
            h = h.cuda()
        
        h_back_dict = {}
        h_back = Variable(torch.zeros(self.params['n_layers'], batch_size, self.rnn_dim))
        if self.params['cuda']:
            h_back = h_back.cuda()  
        for t in range(seq_len - 1, 0, -1):
            h_back_dict[t+1] = h_back
            state_t = data_list[t]
            _, h_back = self.back_gru(state_t, h_back)
        
        curr_p = 0
        _, h = self.gru(data_list[curr_p][:, :, 1:], h)
        while curr_p < seq_len - 1:
            if data_list[curr_p + 1][0, 0, 0] == 1:
                curr_p += 1
                _, h = self.gru(data_list[curr_p][:, :, 1:], h)
            else:
                next_p = curr_p + 1
                while next_p < seq_len and data_list[next_p][0, 0, 0] == 0:
                    next_p += 1
                
                step_size = 1
                while curr_p + 2 * step_size <= next_p and step_size <= self.highest:
                    step_size *= 2
                step_size = step_size // 2
                
                self.interpolate(data_list, curr_p, h, h_back_dict, step_size)
        
        return torch.cat(data_list, dim=0)[:, :, 1:]

    def interpolate(self, data_list, curr_p, h, h_back_dict, step_size):
        #print("interpolating:", len(ret), step_size)
        h_back = h_back_dict[curr_p + 2 * step_size]
        curr_level = self.networks[str(step_size)]
        
        dec_t = curr_level['dec'](torch.cat([h[-1], h_back[-1]], 1))
        dec_mean_t = curr_level['mean'](dec_t)
        if self.stochastic:
            dec_std_t = curr_level['std'](dec_t)
            state_t = reparam_sample_gauss(dec_mean_t, dec_std_t)
        else:
            state_t = dec_mean_t
        
        added_state = state_t.unsqueeze(0)
        has_value = Variable(torch.ones(added_state.shape[0], added_state.shape[1], 1))
        if self.params['cuda']:
            has_value = has_value.cuda()
        added_state = torch.cat([has_value, added_state], 2)
        
        if step_size > 1:
            right = curr_p + step_size
            left = curr_p + step_size // 2
            h_back = h_back_dict[right+1]
            _, h_back = self.back_gru(added_state, h_back)
            h_back_dict[right] = h_back
            
            zeros = Variable(torch.zeros(added_state.shape[0], added_state.shape[1], self.y_dim + 1))
            if self.params['cuda']:
                zeros = zeros.cuda()
            for i in range(right-1, left-1, -1):
                _, h_back = self.back_gru(zeros, h_back)
                h_back_dict[i] = h_back
        
        data_list[curr_p + step_size] = added_state


def num_trainable_params(model):
    total = 0
    for p in model.parameters():
        count = 1
        for s in p.size():
            count *= s
        total += count
    return total


def nll_gauss(mean, std, x):
    pi = Variable(torch.DoubleTensor([np.pi]))
    if mean.is_cuda:
        pi = pi.cuda()
    nll_element = (x - mean).pow(2) / std.pow(2) + 2*torch.log(std) + torch.log(2*pi)
    
    return 0.5 * torch.sum(nll_element)


def reparam_sample_gauss(mean, std):
    eps = torch.DoubleTensor(std.size()).normal_()
    eps = Variable(eps)
    if mean.is_cuda:
        eps = eps.cuda()
    return eps.mul(std).add_(mean)


import argparse
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--path', type=str, required=True, help='data path')
    parser.add_argument('--window', type=int, required=False, default=50, help='imputation window size')
    parser.add_argument('--epoch', type=int, required=False, default=200, help='train epoch')
    parser.add_argument('--gpu', type=int, required=False, default=0, help='whether to use gpu or not')

    args = parser.parse_args()

    naomiIMP = NAMOIimputation(args.path, window_size=args.window, use_gpu= args.gpu)
    naomiIMP.imputation(args.epoch)
    naomiIMP.plot()
    naomiIMP.df.to_csv("result.csv")