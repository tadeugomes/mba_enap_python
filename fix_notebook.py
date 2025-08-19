import json

notebook_path = 'c:\\Projects\\mba_enap\\CD\\Notebooks\\Aula0_Bigquery.ipynb'
fixed_notebook_path = 'c:\\Projects\\mba_enap\\CD\\Notebooks\\Aula0_Bigquery_corrigido.ipynb'

try:
    with open(notebook_path, 'r', encoding='utf-8') as f:
        notebook_content = json.load(f)

    if 'metadata' in notebook_content and 'widgets' in notebook_content['metadata']:
        del notebook_content['metadata']['widgets']
        print("Seção 'widgets' removida dos metadados.")

    with open(fixed_notebook_path, 'w', encoding='utf-8') as f:
        json.dump(notebook_content, f, indent=2)
    
    print(f'Notebook corrigido e salvo em: {fixed_notebook_path}')

except FileNotFoundError:
    print(f'Erro: O arquivo {notebook_path} não foi encontrado.')
except json.JSONDecodeError:
    print('Erro: Falha ao decodificar o JSON do notebook. O arquivo pode estar corrompido.')
except Exception as e:
    print(f'Ocorreu um erro inesperado: {e}')
