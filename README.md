# Recomendação de mapas com regressão linear
Foi implementado um algoritmo de regressão linear utilizando python e sklearn para a predição de novos mapas. A IA foi encaixada no contexto de um jogo que havia sido desenvolvido com a feature de geração procedural de mapas a cada iteração do jogo. 

O jogo se trata de um RPG top-down de ação, o jogador pode aceitar quests de npcs a partir de uma hub (isto é opcional, não impede o jogador de avançar no fluxo do jogo). Para o jogador ter acesso ao mapa gerado proceduralmente ele deve entrar em um portal que permite a personalização do mapa, ou seja, o jogador consegue informar ao algoritmo de geração procedural algumas inputs como: altura, largura, densidade de itens e inimigos, distância entre os objetos e etc. Ao determinar as inputs o jogador será enviado ao mapa gerado proceduralmente a partir das inputs do jogador.

![gif-jogo](https://user-images.githubusercontent.com/43999903/210164689-e29c5c11-802e-485a-8f54-54eda1d306ea.gif)

Após o jogador realizar os objetivos do mapa e terminar a fase gerada ele será enviado para a próxima etapa do fluxo, neta etapa ele irá responder um questionário onde serão coletadas informações sobre a jogada atual, este questionário irá fornecer dados importantes para o algoritmo da regressão posteriormente no fluxo. Após responder o questionário o jogador será enviado para a hub do jogo e o fluxo irá se repetir.

Após a inserção da regressão no jogo o fluxo segue basicamente o mesmo do descrito anteriormente, porém ao finalizar o questionário, todos os dados coletados durante a gameplay do jogador como: tempo no mapa, inimigos derrotados, itens coletados e etc, serão utilizados pela regressão para que ela faça a predição de um novo mapa baseado no último jogado pelo jogador. É levado em consideração como parâmentro de entrada para a regressão o parâmetro "deversão", esta entrada serve para indicar ao algoritmo da regressão o nível de satisfação do jogador no último mapa jogado, desta forma é possível evitar que mapas "ruins" preditos pela regressão sejam passados para o jogador. Mapas com um nível de diversão baixo serão gerados pela regressão pois este algoritmo sempre irá realizar predições a partir da última jogada, ou seja, se o jogador não gostou do mapa jogado a regressão irá gerar um para próximo ao último, por isto que o parâmentro "diversão" é importante. Após a IA retornar o mapa será feita uma validação para verificar se o mapa predito é realmente bom, isto é feito a partir da predição do parãmetro "diversão" feito pela regressão se baseando no mesmo parâmetro que também foi utilizado como entrada.

Se o mapa predito for bom ele será passado para o jogador, caso não seja, será selecionado um mapa aleatório em um buffer de mapas. Este método foi introduzido no jogo para tornar a experiência do jogador melhor, pois com a regressão é possível gerar mapas próximos ao que o jogador gosta, a geração procedural não leva em consireção o gosto do jogador, desta forma ela irá apenas gerar mapas aleatórios. Ambos os métodos funcionando em conjunto permitem a geração de novos mapas mais interessantes para o jogador.

O fluxo em mais baixo nível do projeto pode ser descrito pelas seguintes etapas:

1. Jogo desenvolvido na Unity (aqui temos as mecânicas, assets e a geração procedural).
2. Dataset atualizado em tempo real a cada jogada.
3. Regressão linear (aqui temos a seleção das features, treinamento e geração do modelo treinado).
4. API desenvolvida utilizando o flask + python para comunicação entre jogo e IA.

![tcc-flow](https://user-images.githubusercontent.com/43999903/210164850-ad41a298-f204-4c8d-a543-0b62a8c94f45.jpg)

Entrnando em mais detalhes sobre cada etapa do fluxo simplificado descrito acima. O jogo onde a regressão foi inserido já havia sido desenvolvido utilizando a Unity como engine de desenvolvimento. O jogo já foi explicado anteriormente então explicando melhor o que não havia sido mencionado anterirormente, existem dados de gameplay coletados durante a jogada do jogador nos mapas e os dados de feedback de gameplay coletados no questionário, ambos os tipos de dados são enviados para uma planilha do google que serve como base de dados para a IA, pois nela temos os dados de todas as jogadas de todos os jogadores que já jogaram o jogo. 

Desta forma, a regressão terá acesso a uma base de treino mais robusta com uma variedade de dados maior, não ficando limitada ao viés de um jogador. No algoritmo da regressão será feito o import da base de dados e a mesma será splitada em uma base de treino e uma base de teste. É realizada a filtragem das features que serão utilizadas pela regressão a partir de um heatmap, este nos indica quais features se correlacionam melhor, quanto melhor a correlação entre as features melhor serão os resultados gerados pela regressão, abaixo exemplos de heatmaps com alguns dados utilizados para testes:

![heatmap-t1](https://user-images.githubusercontent.com/43999903/210165049-915ec452-b3c8-41aa-8165-e07aeb3eb887.png)

![heatmap-t2](https://user-images.githubusercontent.com/43999903/210165056-27eaffd9-dd4a-4584-9f2b-0019b5d8f101.png)

Quanto mais quente a cor entre as features melhor a correlção. Quanto mais fria, pior a correlação.

Além do código desenvolvido para a regressão foi também desenvolvida uma API utilizando python e o microframework flask para a comunicação entre o jogo e o modelo treinado da regressão. A API recebe na requisição o último mapa jogado pelo jogador e mais alguns dados que são usados pela regressão para a predição de um novo mapa, dentro da API o modelo treinado (modelo salvo no formato joblib) da IA é executado e após a execução é retornado como resposta um json que contém o novo mapa predito.

Na unity foi necessário alterar alguns códigos do jogo base para que o novo fluxo funcionasse corretamente e também foi adicionado um script para realizar as requisições para a API e formatar os dados corretamente, tanto para o envio da requisição quanto para o recebimento da resposta. Também foi realizada a verificação do novo mapa gerado, desta forma evitando que um mapa ruim seja passado ao jogador e também foram adicionados métodos que montam as entradas no formato correto para a IA.

Por fim, os dados gerados pela regressão serão utilizados pela geração procedural como a base para um novo mapa. Abaixo temos duas tabelas, na primeira cada linha representa um mapa de entrada com os dados de entrada importantes para a regressão. Na segunda tabela temos os mapas gerados pela regressão + geração procedural:

![map-input-t2](https://user-images.githubusercontent.com/43999903/210165330-ff686442-9b37-4abc-81f9-38b8c61f378d.png)
![map-regression-t2](https://user-images.githubusercontent.com/43999903/210165333-0d94ef14-2d86-4a97-be07-9f376c3b76b1.png)

Pelas tabelas é possível notar que em alguns casos os mapas preditos foram bem parecidos e em outros os mapas foram distintos, também é possível verificar que o valor predito para maxItens é sempre 12 independente da entrada, estes problemas acontecem por conta do dataset que foi utilizado para o treinamento. O dataset contém poucas amostras e baixa variabilidade de amostras, ou seja, muitas amostras são iguais ou pouco distintas.

Para melhor compreensão do que foi explicado indico os seguintes materiais:

1. Vídeo onde explico o fluxo no jogo: https://youtu.be/9bHxlo3Y1is
2. Texto contendo explicações mais detalhadas de todo o proejto: [TCC - Kevin Oliveira.pdf](https://github.com/nivek14/Game-AI-Regression/files/10328520/TCC.-.Kevin.Oliveira.pdf)

Detalhes técnicos:

1. Versão da Unity usada: 2021.3.0f1
2. Para que o jogo funcione com a Regresão, rodar o comando python app.py para que a API rode e as chamadas para a mesma ocorram corretamente.






