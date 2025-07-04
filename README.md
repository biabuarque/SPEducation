
## Grupo
- Ana Beatriz Silva Buarque (257241)
- Lucas Ribeiro Bortoletto (173422)


# Justificativa
---
# Recebemos o cenário B. Por que MongoDB seria a melhor resposta?

## Armazenamento de arquivos

### Estrutura de dados flexível

O MongoDB é excelente em armazenar esquemas dinâmicos, inclusive com arrays, bem como permite a inclusão de novos campos em documentos sem a necessidade de alterações no esquema ou migrações. Isso é possível graças à sua arquitetura orientada a documentos, onde cada documento é armazenado em formato BSON (Binary JSON). 

Desde que sigamos padrões de projeto adequados, podemos armazenar entidades e seus dados agregados relacionados em um único documento. Isso reduz a necessidade de operações *join* complexas, comuns em bancos de dados relacionais, e melhora a eficiência das operações de leitura e escrita. Essa flexibilidade é crucial para sistemas que lidam com dados semiestruturados e em constante evolução.

### Suporte a replicação, particionamento e balanceamento de carga

O MongoDB utiliza ***replica sets*** para assegurar a continuidade do serviço mesmo diante de falhas. Cada conjunto é composto por um nó primário, responsável por todas as operações de gravação, e um ou mais nós secundários, que replicam os dados do primário. Caso o nó primário apresente problemas, um dos nós secundários é automaticamente promovido a primário, garantindo a continuidade das operações sem interrupções significativas.

A **escalabilidade horizontal** desse banco é garantida por meio do particionamento de dados (***sharding***), distribuindo coleções grandes entre múltiplos servidores. Cada *shard* é responsável por uma parte dos dados, permitindo que o sistema lide com grandes volumes de informações e altas taxas de requisições. Analogamente, para armazenar arquivos grandes que excedem o limite de 16 MB do BSON, o MongoDB oferece o **GridFS**, que divide arquivos em partes menores chamadas *chunks* e armazena cada uma como um documento separado. Essas estratégias permitem o armazenamento eficiente de arquivos grandes, como imagens, vídeos e documentos, diretamente no banco de dados, facilitando o gerenciamento e a recuperação desses arquivos.

A arquitetura do MongoDB fornece **balanceamento de carga **automático**, em que as requisições de diferentes clientes são distribuídas nos nós disponíveis para otimizar a utilização de recursos e melhorar a performance. Para o nosso cenário, em que há muitos acessos simultâneos que requerem entidades completas, a união da arquitetura orientada a documentos com o *load balancing* automático é muito vantajosa.

## Processamento de Consultas

O MongoDB é projetado para oferecer **baixa latência em operações CRUD** (Criação, Leitura, Atualização e Exclusão). Isso é alcançado por meio de técnicas como indexação eficiente, armazenamento em memória e operações assíncronas. 

No contexto de indexação, o MongoDB suporta diversas estratégias, incluindo índices compostos e geoespaciais, para otimizar o desempenho das consultas. Por exemplo, ao utilizar índices compostos, é possível otimizar consultas que envolvem múltiplos campos, reduzindo significativamente o tempo de resposta e melhorando a experiência do usuário em aplicações de alta demanda. Já o motor de armazenamento WiredTiger oferece uma opção de armazenamento em memória, reduzindo a I/O de disco e melhorando as operações de leitura e gravação. 

O *Aggregation Framework* do MongoDB permite realizar transformações e cálculos complexos diretamente no banco de dados, utilizando um pipeline composto por estágios sequenciais. Cada estágio executa uma operação específica, como filtragem, agrupamento ou ordenação, proporcionando flexibilidade e eficiência no processamento de dados. Essa abordagem reduz a necessidade de manipulação extensiva no lado do cliente, otimizando o desempenho geral do sistema.  

Além disso, o MongoDB oferece suporte a expressões agregadas personalizadas, como **$accumulator** e **$function**, introduzidas na versão 4.4, permitindo maior flexibilidade na definição de operações complexas. Aliando isso com o *framework* já existente, a manipulação de entidades completas, incluindo a execução de operações complexas, é realizada satisfatoriamente.

## Processamento e Controle de Transações

Na versão 4.0, foram implementadas as transações com propriedades ACID (Atomicidade, Consistência, Isolamento e Durabilidade) no MongoDB, que permitem que operações envolvendo múltiplos documentos e coleções sejam executadas de forma confiável e consistente. Aliando isso com os *replica sets*, que garantem a recuperação diante de falhas, o volume alto de acessos simultâneos exigidos pelo cenário será possível.

## Mecanismos de Recuperação e Segurança

Além dos *replica sets*, o MongoDB oferece ferramentas como `mongodump` e `mongorestore` para realizar backups e restaurações de dados, facilitando ainda mais a recuperação em caso de falhas.

A segurança no MongoDB é garantida mediante a incorporação de uma série de recursos para proteger os dados armazenados. A autenticação é baseada no mecanismo SCRAM, com suporte adicional para LDAP e certificados x.509, garantindo a verificação adequada das identidades dos usuários. O controle de acesso é implementado por meio de *Role-Based Access Control* (RBAC), permitindo atribuir permissões granulares a usuários e funções, assegurando que apenas usuários autorizados possam acessar ou modificar dados sensíveis. A criptografia é aplicada tanto em repouso quanto em trânsito, utilizando protocolos seguros para proteger os dados durante a transmissão e enquanto armazenados no banco de dados. Além disso, o MongoDB oferece funcionalidades de auditoria, permitindo o rastreamento detalhado das operações realizadas no banco de dados, o que é essencial para monitoramento e conformidade regulatória.
