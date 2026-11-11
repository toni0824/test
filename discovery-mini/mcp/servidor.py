"""Servidor MCP mínimo sobre stdio; apenas biblioteca padrão Python."""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from contar_palavras import contar_palavras


def responder(pedido: dict) -> dict | None:
    if "id" not in pedido:
        return None  # Notificações JSON-RPC não recebem resposta.
    resposta = {"jsonrpc": "2.0", "id": pedido["id"]}
    metodo = pedido.get("method")
    if metodo == "initialize":
        resposta["result"] = {
            "protocolVersion": "2024-11-05",
            "capabilities": {"tools": {}},
            "serverInfo": {"name": "contador-mcp", "version": "1.0.0"},
        }
    elif metodo == "ping":
        resposta["result"] = {}
    elif metodo == "tools/list":
        resposta["result"] = {"tools": [{
            "name": "contar_palavras",
            "description": "Conta segmentos de texto separados por espaços.",
            "inputSchema": {
                "type": "object",
                "properties": {"texto": {"type": "string"}},
                "required": ["texto"],
                "additionalProperties": False,
            },
        }]}
    elif metodo == "tools/call":
        params = pedido.get("params", {})
        argumentos = params.get("arguments", {})
        if params.get("name") != "contar_palavras":
            resposta["error"] = {"code": -32602, "message": "Ferramenta desconhecida"}
        elif not isinstance(argumentos, dict) or not isinstance(argumentos.get("texto"), str):
            resposta["error"] = {"code": -32602, "message": "texto deve ser string"}
        else:
            resposta["result"] = {"content": [{
                "type": "text", "text": str(contar_palavras(argumentos["texto"]))
            }], "isError": False}
    else:
        resposta["error"] = {"code": -32601, "message": "Método desconhecido"}
    return resposta


if __name__ == "__main__":
    for linha in sys.stdin:
        try:
            pedido = json.loads(linha)
        except json.JSONDecodeError:
            resultado = {"jsonrpc": "2.0", "id": None,
                         "error": {"code": -32700, "message": "JSON inválido"}}
        else:
            if not isinstance(pedido, dict) or pedido.get("jsonrpc") != "2.0" or not isinstance(pedido.get("method"), str):
                resultado = {"jsonrpc": "2.0", "id": None,
                             "error": {"code": -32600, "message": "Pedido inválido"}}
            else:
                resultado = responder(pedido)
        if resultado is not None:
            print(json.dumps(resultado), flush=True)
