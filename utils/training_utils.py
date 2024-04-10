import torch
import torch.optim as optim
import torch.nn as nn

class Trainer():
    def __init__(self,model,lr=0.001, momentum=0.9,log = False) -> None:
        
        self.log = log
        self.model = model

        # baseline loss function
        self.criterion = nn.CrossEntropyLoss()
        self.optimizer = optim.SGD(self.model.parameters(), lr=lr, momentum=momentum)

        if self.log:
            print('[Trainer]: Trainer initialized')

        # if self.log:
        #     print('[Trainer]: Parameter summary:')
        #     print(summarizeWeights(self.model))

    def training_loop(self,inputs,labels) -> "loss":

        inputs = torch.Tensor(inputs)
        labels = torch.Tensor(labels)

        # zero the parameter gradients
        self.optimizer.zero_grad()

        # forward pass
        outputs = self.model(inputs)
        # print(outputs)

        # calculate baseline loss + modulated regularization value
        loss = self.criterion(outputs, labels)

        # calculate gradients with respect to loss
        loss.backward()

        # apply gradients to parameters
        self.optimizer.step()

        # return loss value for analysis
        return loss.item()
    
    def training_epoch(self,epochs,trainloader):
        losses = []

        for epoch in range(epochs):

            print(f'[Trainer]: Epoch {epoch}')

            for i, (inputs,labels) in enumerate(trainloader, 0):

                # limit training time for debugging purposes
                # if i > 5:
                #     break
                
                loss = self.training_loop(inputs,labels)
            
                losses.append(loss)

        return losses
    
def summarize(values):
    summary = {
        'mean': sum(values) / len(values),
        'min': min(values),
        'max': max(values),
        'std_dev': (sum((x - (sum(values) / len(values))) ** 2 for x in values) / len(values)) ** 0.5
    }
    return summary

def summarizeWeights(model):
    a = [(name, param) for name, param in model.named_parameters()]
    b = a[0][1].data.numpy().reshape(-1)
    return summarize(b)