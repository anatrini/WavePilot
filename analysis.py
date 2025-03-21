# import os
# import json
# import re
# import pandas as pd
# import plotly.express as px
# from glob import glob

# # Path principali ai log diretti (senza transfer learning)
# logs_path = {
#     'adaptiverb': "./logs/info_total/adaptiverb",
#     'obxd': "./logs/info_total/adaptiverb"
# }

# param_regex = re.compile(r"{.*}")

# def extract_configs(log_folder, param_type):
#     all_configs = []
#     files = glob(os.path.join(log_folder, "*.log"))
    
#     for file in files:
#         with open(file, 'r') as f:
#             for line in f:
#                 if param_type == 'VAE' and "'validation_error'" in line:
#                     match = param_regex.search(line)
#                     if match:
#                         config = json.loads(match.group(0).replace("'", '"'))
#                         all_configs.append(config)
#                 elif param_type == 'RBF' and "'validation_distance'" in line:
#                     match = param_regex.search(line)
#                     if match:
#                         config = json.loads(match.group(0).replace("'", '"'))
#                         all_configs.append(config)

#     return pd.DataFrame(all_configs)

# # Carica e combina dati da entrambi gli strumenti
# vae_configs, rbf_configs = [], []

# for instrument, path in logs_path.items():
#     df_vae = extract_configs(path, 'VAE')
#     df_vae['instrument'] = instrument
#     vae_configs.append(df_vae)

#     df_rbf = extract_configs(path, 'RBF')
#     df_rbf['instrument'] = instrument
#     rbf_configs.append(df_rbf)

# vae_df = pd.concat(vae_configs, ignore_index=True)
# rbf_df = pd.concat(rbf_configs, ignore_index=True)

# # VISUALIZZAZIONI VAE
# fig_vae = px.parallel_coordinates(
#     vae_df,
#     dimensions=['num_epochs', 'learning_rate', 'weight_decay', 'n_layers', 'layer_dim', 'kl_beta', 'mse_beta'],
#     color='validation_error',
#     title='Distribuzione dei parametri VAE (entrambi gli strumenti)',
#     color_continuous_scale=px.colors.sequential.Viridis
# )
# fig_vae.show()

# # VISUALIZZAZIONI RBF
# fig_rbf = px.parallel_coordinates(
#     rbf_df,
#     dimensions=['smoothing', 'epsilon', 'degree'],
#     color='validation_distance',
#     title='Distribuzione dei parametri RBF (entrambi gli strumenti)',
#     color_continuous_scale=px.colors.sequential.Viridis
# )
# fig_rbf.show()

# # DISTRIBUZIONE DEI KERNEL RBF
# fig_kernel = px.histogram(rbf_df, x='kernel', color='instrument', barmode='group',
#                           title='Distribuzione del Kernel RBF')
# fig_kernel.show()

# # Ora puoi salvare i risultati aggregati per analisi manuale e scelta finale degli intervalli ristretti:
# vae_df.to_csv("combined_vae_configs.csv", index=False)
# rbf_df.to_csv("combined_rbf_configs.csv", index=False)

import os
import json
import re
import pandas as pd
import plotly.express as px
from glob import glob

# Paths ai log diretti (senza transfer learning)
logs_path = {
    'adaptiverb': "./logs/info_total/adaptiverb",
    'obxd': "./logs/info_total/obxd"
}

param_regex = re.compile(r"{.*}")

def extract_configs(log_folder, param_type):
    all_configs = []
    files = glob(os.path.join(log_folder, "*.log"))
    
    for file in files:
        with open(file, 'r') as f:
            for line in f:
                if param_type == 'VAE' and "'validation_error'" in line:
                    match = param_regex.search(line)
                    if match:
                        config = json.loads(match.group(0).replace("'", '"'))
                        all_configs.append(config)
                elif param_type == 'RBF' and "'validation_distance'" in line:
                    match = param_regex.search(line)
                    if match:
                        config = json.loads(match.group(0).replace("'", '"'))
                        all_configs.append(config)

    return pd.DataFrame(all_configs)

# Carica e combina dati da entrambi gli strumenti
vae_configs, rbf_configs = [], []

for instrument, path in logs_path.items():
    df_vae = extract_configs(path, 'VAE')
    df_vae['instrument'] = instrument
    vae_configs.append(df_vae)

    df_rbf = extract_configs(path, 'RBF')
    df_rbf['instrument'] = instrument
    rbf_configs.append(df_rbf)

vae_df = pd.concat(vae_configs, ignore_index=True)
rbf_df = pd.concat(rbf_configs, ignore_index=True)

# Converte la funzione di attivazione da categorica a numerica
activation_mapping = {'ReLU': 0, 'LeakyReLU': 1, 'ELU': 2, 'GELU': 3}
vae_df['activation_numeric'] = vae_df['activation_function'].map(activation_mapping)

# VISUALIZZAZIONI VAE con funzione di attivazione integrata
fig_vae = px.parallel_coordinates(
    vae_df,
    dimensions=[
        'num_epochs',
        'learning_rate',
        'weight_decay',
        'n_layers',
        'layer_dim',
        'activation_numeric',  # Ora inclusa!
        'kl_beta',
        'mse_beta'
    ],
    color='validation_error',
    title='Distribuzione dei parametri VAE (inclusa activation function)',
    color_continuous_scale=px.colors.sequential.Viridis,
    labels={'activation_numeric': 'Activation Function'}
)

# Modifica manualmente le etichette numeriche in quelle delle funzioni di attivazione
fig_vae.update_layout(
    coloraxis_colorbar=dict(title="Validation Error"),
)

fig_vae.update_traces(
    dimensions=[
        {}, {}, {}, {}, {},
        dict(tickvals=[0, 1, 2, 3], ticktext=['ReLU', 'LeakyReLU', 'ELU', 'GELU']),
        {}, {}
    ]
)

fig_vae.show()

# VISUALIZZAZIONI RBF (senza modifiche)
fig_rbf = px.parallel_coordinates(
    rbf_df,
    dimensions=['smoothing', 'epsilon', 'degree'],
    color='validation_distance',
    title='Distribuzione dei parametri RBF (entrambi gli strumenti)',
    color_continuous_scale=px.colors.sequential.Viridis
)
fig_rbf.show()

# DISTRIBUZIONE DEI KERNEL RBF (senza modifiche)
fig_kernel = px.histogram(rbf_df, x='kernel', color='instrument', barmode='group',
                          title='Distribuzione del Kernel RBF')
fig_kernel.show()

# Salva risultati aggregati
vae_df.to_csv("combined_vae_configs.csv", index=False)
rbf_df.to_csv("combined_rbf_configs.csv", index=False)
