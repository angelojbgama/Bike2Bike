import os
import shutil

def remover_pycache(diretorio_base='.'):
    total_removidas = 0
    for raiz, diretorios, arquivos in os.walk(diretorio_base):
        for nome in diretorios:
            if nome == '__pycache__':
                caminho_completo = os.path.join(raiz, nome)
                try:
                    shutil.rmtree(caminho_completo)
                    print(f"[OK] Removido: {caminho_completo}")
                    total_removidas += 1
                except Exception as e:
                    print(f"[ERRO] Falha ao remover {caminho_completo}: {e}")
    print(f"\nTotal de pastas '__pycache__' removidas: {total_removidas}")

if __name__ == '__main__':
    remover_pycache()
