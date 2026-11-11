"""Contagem determinística: uma palavra por segmento não vazio separado por espaço."""

import argparse


def contar_palavras(texto: str) -> int:
    return len(texto.split())


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("texto")
    args = parser.parse_args()
    print(contar_palavras(args.texto))
