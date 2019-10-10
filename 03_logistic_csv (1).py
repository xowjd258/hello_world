import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim


xy = np.loadtxt('data-03-diabetes.csv', delimiter=',', dtype=np.float32)
x_data = xy[:, 0:-1]
y_data = xy[:, [-1]]
x_train = torch.FloatTensor(x_data)
y_train = torch.FloatTensor(y_data)


class BinaryClassifier(nn.Module):
    def __init__(self):
        super().__init__()
        self.linear = nn.Linear(8, 1)
        self.sigmoid = nn.Sigmoid()

    def forward(self, x):
        return self.sigmoid(self.linear(x))

model = BinaryClassifier()


# optimizer lr = 10 vs 1 vs 0.1 vs 0.01
optimizer = optim.SGD(model.parameters(), lr=0.01)

nb_epochs = 20000
for epoch in range(nb_epochs + 1):

    # cost
    hypothesis = model(x_train)
    cost = F.binary_cross_entropy(hypothesis, y_train)

    # gradient descent
    optimizer.zero_grad()
    cost.backward()
    optimizer.step()

    # accuracy
    prediction = (hypothesis >= torch.FloatTensor([0.5]))
    correct_prediction = (prediction.float() == y_train)
    accuracy = correct_prediction.sum().item() / len(correct_prediction)
    

    # check progress
    if epoch % 100 == 0:
        print(f'Epoch {epoch:4d}/{nb_epochs} Cost: {cost.item():.6f} '
        f'Accuracy: {accuracy*100:.6f}')
