import plotly.graph_objects as go
from plotly.subplots import make_subplots

import torch
from torch import nn


# Read and get best hyperparams from log session
def get_hyperparams_from_log(log_file):
    with open(log_file, 'r') as f:
        lines = f.readlines()

    params = {}
    for line in lines:
        if "Best autoencoder hyperparams" in line:
            # Get autoencoder's best hyperp fomr log
            params_str = line.split("Best autoencoder hyperparams: ")[1].split(" with")[0]
            params['autoencoder'] = eval(params_str)
        elif "Best interpolator params" in line:
            # Get interpolator's best hyperp fomr log
            params_str = line.split("Best interpolator params ")[1].split(" with")[0]
            params['interpolator'] = eval(params_str)

    return params

# Get activation function module from string
def get_activation_function(activation_name):
    activation_functions = {
        'ReLU': nn.ReLU(),
        'Sigmoid': nn.Sigmoid(),
        'Tanh': nn.Tanh()
    }
    return activation_functions.get(activation_name, None)


# Compute loss for optimization
def compute_validation_error(model, criterion, val_data):
    with torch.no_grad():
        val_data = val_data.drop(['ID', 'PRESET_NAME'], axis=1)
        val_data = torch.tensor(val_data.values).float()
        _, output = model(val_data)
        loss = criterion(output, val_data)
    return loss.item()


# Plot autoencoder e interpolator performances during optimization
def plot_losses(model_trials, interpolator_trials):
    model_errors = []
    interpolator_errors = []

    for trial in model_trials:
        #model_errors.append(trial.user_attrs['validation_errors'])
        model_errors.append(trial.value)
    for trial in interpolator_trials:
        interpolator_errors.append(trial.value)

    # Create plot
    fig = make_subplots(rows=1, cols=2)
    # Add traces to the plot
    fig.add_trace(go.Scatter(y=model_errors, mode='lines', name=f'Autoencoder metrics'), row=1, col=1)
    fig.add_trace(go.Scatter(y=interpolator_errors, mode='lines', name=f'Interpolator metrics'), row=1, col=2)

    fig.update_layout(height=600, width=1200, title='Metrics during optimization')
    fig.update_xaxes(title_text='Trials', row=1, col=1)
    fig.update_yaxes(title_text='Target', row=1, col=1)
    fig.update_xaxes(title_text='Trials', row=1, col=2)
    fig.update_yaxes(title_text='Target', row=1, col=2)
    fig.show()
