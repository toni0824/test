# Discovery Mini

Fixture de descoberta estática com cinco componentes intencionais.
Requer Python 3.10+; não precisa de dependências Python externas.

Abre o Claude Code na raiz deste projeto para disponibilizar as definições
locais. O agente e a skill são declarados; a execução depende do Claude Code.
A ligação MCP usa caminhos relativos: inicia o cliente na raiz do projeto.

Experimenta o script:

```sh
python3 scripts/contar_palavras.py "um dois três"
```

O resultado esperado é `3`. O servidor pode ser iniciado com:

```sh
python3 mcp/servidor.py
```

Recebe mensagens MCP JSON-RPC, uma por linha em stdin, e responde em stdout.
É uma implementação mínima para testes locais, sem serviços externos.
