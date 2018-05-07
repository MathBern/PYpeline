# PYpeline

O PYpeline é uma pipeline simples que trata dados astronômicos em formato FITS.

O pacote foi escrito em linguagem Python 3.6, no ambiente Anaconda 5.1.

## Instalação

### Dependências

O PYpeline depende de pacotes e módulos para funcionar. São eles:

Numpy
Pandas
Astropy
Os
Glob
Numba

Portanto, certifique-se que o computador os tenha. Recomenda-se que se instale as dependências antes de instalar o PYpeline.

### Organização do Diretório da Observação

### Instruções de Instalação

Uma vez instalado as dependências, para instalar o PYpeline, basta clonar o projeto do GitHub para um diretório qualquer e executar o arquivo setup.py.

Por exemplo, estando no diretório principal do PYpeline, executar:

```
python setup.py 
```

ou

```
sudo python setup.py 
```

Pronto! O PYpeline está instalado!


## Usando o PYpeline

O PYpeline é um módulo usual contendo funções apenas. Para importa-lo em um código basta inserir, por exemplo:

```
import PYpeline as PYl
```

### Funções Contidas

As funções cujos nomes começam em letra maiúscula são as *funções principais* que fazem diretamente o que se propõe a fazer o PYpeline. Em contrapartida, as começadas em letra minúscula são funcões que são utilizadas pelas *funções principais*.

```
CreateMasterBias(observation_directory)
```
Cria um bias combinado, pela mediana, a partir das imagens de bias contidos na pasta *bias*.

```
normalize_by_mean(array)
```
Normaliza um array (que podem ser os dados de um arquivo FITS) pela média.

```
CreateMasterFlat(obs_dir)
```
Cria um flat combinado a partir das imagens de flat, contidos na pasta *flat*.

```
ReduceCompletely(observation_directory, name, combine_images) 
```
Efetua a redução completa de uma imagem FITS de ciência, subtraindo bias e nivelando pelo flat.

```
open_and_convert_to_f64(image_FITS)
```
Abre um arquivo .fits e converte seus dados numéricos para float64.

```
save_fits(array_img, outfile, image_header)
```
