# YTDownloader
**Objetivo**

 O objetivo deste projeto é criar uma aplicação em python de **download e conversão
 de mídias, com ênfase em vídeos do YouTube e músicas**. A aplicação é projetada
 para permitir ao usuário baixar vídeos e músicas do YouTube, converter os vídeos
 em formatos de áudio e gerenciar esses arquivos de mídia.
 Utilização de Threads e Semáforos
 
 O projeto utiliza threads e semáforos para melhorar o desempenho e a eficiência das
 operações de download, conversão e reprodução de mídia. As threads são empregadas
 para processar múltiplas operações simultaneamente, enquanto os semáforos são
 utilizados para sincronizar e controlar o acesso a recursos compartilhados.
 Baixar Vídeo do YouTube
 
 A função **baixando_videos()** é responsável por baixar vídeos do YouTube. Ela emprega
 semáforos para garantir que apenas uma thread por vez acesse recursos críticos, como a
 lista de URLs de vídeo e a barra de progresso.
 Nesta função, os links de vídeos são mantidos em uma lista, e durante a execução, essa
 lista é dividida pela metade. Cada metade é designada para uma thread, permitindo a
 execução simultânea de múltiplas operações de download.
 
 Ao iniciar, cada thread entra em uma fila para acessar os recursos compartilhados, como a
 lista de URLs de vídeo. Em uma situação de concorrência, apenas uma das threads
 consegue adquirir um semáforo, permitindo-lhe iniciar uma requisição de download para um
 elemento da lista.
 
 Após a conclusão da requisição, o semáforo é liberado, possibilitando que outra thread
 entre em ação e inicie sua própria requisição. Esse processo continua até que todas as
 requisições de download sejam concluídas.
 
 Essa abordagem de divisão de tarefas entre threads, combinada com o uso de semáforos
 para controlar o acesso aos recursos compartilhados, resulta em um processo eficiente e
 paralelo de download de vídeos do YouTube.
 
 **Baixar Áudio do YouTube**
 
 Similar à função de baixar vídeo, a função **baixando_musicas()** realiza downloads de
 áudios do YouTube. Ela utiliza semáforos para sincronizar o acesso à lista de URLs de
 áudio e à barra de progresso.
 
 Na função baixar_musicas(), os links de áudios do YouTube são armazenados em uma lista.
 Durante a execução, essa lista é dividida pela metade, com cada metade sendo atribuída a
 uma thread. Esse arranjo permite a execução simultânea de várias operações de download
 de áudio.
 
 Ao iniciar, cada thread entra em uma fila para acessar os recursos compartilhados, incluindo
 a lista de URLs de áudio. Em uma situação de concorrência, apenas uma das threads
 consegue adquirir um semáforo, permitindo-lhe iniciar uma requisição de download para um
 elemento específico da lista.
 
 Após a conclusão da requisição, o semáforo é liberado, possibilitando que outra thread
 entre em ação e inicie sua própria requisição. Esse ciclo continua até que todas as
 requisições de download de áudio sejam concluídas.
 
 Essa estratégia de divisão de tarefas entre threads, aliada ao uso de semáforos para
 controlar o acesso aos recursos compartilhados, resulta em um processo eficiente e
 paralelo de download de áudios do YouTube. Todos os vídeos baixados, são salvos no
 mesmo diretório onde está o arquivo “TrabalhoSO.py”, criando uma pasta saída(caso ela
 não exista) e uma pasta Vídeo(caso não exista) dentro da pasta “saída”.
 
 **Conversão de Vídeo para Áudio**
 
 Na função de conversão de vídeo para áudio, denominada converter_videos_para_mp3(), o
 processo segue uma lógica semelhante à descrita anteriormente. Primeiramente, os vídeos
 disponíveis são divididos entre duas threads, permitindo a execução simultânea de múltiplas
 conversões.
 Cada thread, ao iniciar, tenta adquirir um semáforo, o que lhe concede permissão para
 acessar a lista de vídeos a serem convertidos. Em uma situação de concorrência, apenas
 uma das threads consegue acesso ao semáforo e inicia uma conversão de vídeo para
 áudio.
 Após a conclusão da conversão de um vídeo, o semáforo é liberado, permitindo que outra
 thread entre em ação e inicie sua própria conversão. Esse processo continua até que todas
 as conversões de vídeo para áudio sejam concluídas.
 
 Essa abordagem de divisão de tarefas entre threads, combinada com o uso de semáforos
 para controlar o acesso aos recursos compartilhados, resulta em um processo eficiente e
 paralelo de conversão de vídeos para áudios. Todos os audios baixados, são salvos no
 mesmo diretório onde está o arquivo “TrabalhoSO.py”, criando uma pasta saída(caso ela
 não exista) e uma pasta Música(caso não exista) dentro da pasta “saída”.
 
 **Conversão de Áudios para a Reprodução**
 
 Na função de converter músicas baixadas para reproduzir, chamada
 **converter_musicas_e_reproduzir()**, há uma integração eficaz do uso de semáforos,
 multithreading e funcionalidade da aplicação. Esta função desempenha um papel crucial no
 fluxo de trabalho do aplicativo, pois não apenas converte os arquivos de áudio baixados
 para um formato adequado à reprodução, mas também inicia a reprodução dessas músicas
 convertidas.
 
 Antes de iniciar a conversão, a função verifica se há uma pasta de saída designada para as
 músicas convertidas, ou seja, dentro da pasta “saída” é guardada em uma pasta
 “Músicas_Convertidas”. Se a pasta não existir, ela é criada. Após isso, a função verifica a
 pasta onde os arquivos de áudio foram baixados. Em seguida, seleciona todos os arquivos
 com a extensão ".mp4", pois esses são os arquivos baixados que precisam ser convertidos.
 
 Divisão do trabalho entre threads: Os arquivos de áudio são divididos em duas partes
 iguais, que são atribuídas a duas threads diferentes para realizar a conversão. Isso permite
 que múltiplas conversões ocorram simultaneamente, melhorando o desempenho e a
 eficiência do processo. Cada thread inicia a conversão dos arquivos de áudio atribuídos a
 ela. Durante esse processo, um semáforo é utilizado para garantir que apenas uma thread
 por vez acesse e converta os arquivos. Isso é importante para evitar conflitos de acesso aos
 recursos compartilhados e garantir a consistência dos dados.
 
 Uma barra de progresso é exibida para acompanhar o progresso da conversão. Cada vez
 que um arquivo é convertido com sucesso, a barra de progresso é atualizada para refletir o
 avanço do processo. Após a conclusão da conversão, as músicas convertidas estão prontas
 para serem reproduzidas.
 
 **Reprodução de Música**
 
 Na função de reprodução de música, chamada **reproduzir_musica()**, ocorre um processo
 peculiar que merece destaque. Quando um áudio é selecionado para reprodução, a função
 utiliza um semáforo para garantir que apenas uma instância do áudio seja manipulada por
 vez. Isso significa que enquanto um áudio está sendo reproduzido, o semáforo impede que
 outras operações, como escrita ou modificação do arquivo de áudio específico, ocorram
 simultaneamente.
 
 Essa abordagem é crucial para evitar possíveis conflitos de acesso ao arquivo de áudio
 durante a reprodução. Ao utilizar um semáforo para controlar a reprodução, garantimos que
 apenas uma instância do áudio seja ativa em determinado momento, mantendo a
 integridade dos dados e a consistência do processo de reprodução.
 
 Assim, durante a reprodução de música, o semáforo desempenha um papel fundamental ao
 garantir a exclusividade do acesso ao arquivo de áudio, evitando potenciais problemas de
 concorrência e garantindo uma reprodução suave e sem interrupções
