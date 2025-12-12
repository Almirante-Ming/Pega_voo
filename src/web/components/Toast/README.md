# 🍞 Toast Component

Sistema de notificações toast genérico com suporte para diferentes tipos de mensagens.

## 📦 Instalação

O Toast já está configurado no layout padrão (`layouts/default.vue`), então você pode usá-lo em qualquer página sem configuração adicional.

## 🚀 Como Usar

### Importar o composable

```typescript
import { useToast } from '@/composables/useToast'

const toast = useToast()
```

### Exemplos de Uso

#### ✅ Toast de Sucesso

```typescript
// Forma 1: String simples (usa título padrão "Sucesso!")
toast.success('Dados salvos com sucesso!')

// Forma 2: Objeto com parâmetros nomeados
toast.success({ 
  mensagem: 'Usuário criado!',
  titulo: 'Bem-vindo!' 
})

// Forma 3: Com duração personalizada
toast.success({ 
  mensagem: 'Login realizado!',
  duracao: 3000 
})

// Forma 4: Parâmetros em qualquer ordem
toast.success({ 
  duracao: 2000,
  titulo: 'Sucesso!',
  mensagem: 'Operação concluída'
})
```

#### ❌ Toast de Erro

```typescript
// String simples (usa título padrão "Erro!")
toast.error('Não foi possível salvar os dados')

// Com título personalizado
toast.error({ 
  mensagem: 'Usuário ou senha incorretos',
  titulo: 'Falha no login' 
})

// Com duração personalizada
toast.error({ 
  mensagem: 'Erro ao processar requisição',
  duracao: 7000 
})
```

#### ⚠️ Toast de Aviso

```typescript
// String simples (usa título padrão "Atenção!")
toast.warning('Alguns campos não foram preenchidos')

// Com título personalizado
toast.warning({ 
  mensagem: 'Verifique os dados antes de continuar',
  titulo: 'Validação' 
})

// Com duração personalizada
toast.warning({ 
  mensagem: 'Sessão expirando em breve',
  duracao: 10000 
})
```

#### ℹ️ Toast Informativo

```typescript
// String simples (sem título padrão)
toast.info('Nova atualização disponível')

// Com título personalizado
toast.info({ 
  mensagem: 'O sistema será atualizado',
  titulo: 'Manutenção Programada' 
})

// Com duração personalizada
toast.info({ 
  mensagem: 'Processando em segundo plano',
  duracao: 4000 
})
```

#### 🎨 Toast Customizado

```typescript
toast.show({
  type: 'success',
  title: 'Título Customizado',
  message: 'Mensagem personalizada',
  duration: 6000 // 0 = não fecha automaticamente
})
```

## 💡 Exemplos Práticos

### Uso em Formulário de Login

```typescript
<script setup lang="ts">
import { useToast } from '@/composables/useToast'

const toast = useToast()
const { execute, error } = useApi('post', '/login')

async function login() {
  try {
    await execute(params)
    toast.success({ mensagem: 'Login realizado com sucesso!' })
    router.push('/dashboard')
  } catch (err) {
    toast.error({ 
      mensagem: 'Usuário ou senha incorretos',
      titulo: 'Erro no login' 
    })
  }
}
</script>
```

### Uso em Cadastro

```typescript
<script setup lang="ts">
import { useToast } from '@/composables/useToast'

const toast = useToast()

async function cadastrar() {
  if (!formValido.value) {
    toast.warning({ mensagem: 'Preencha todos os campos obrigatórios' })
    return
  }

  try {
    await execute(dados)
    toast.success({ 
      mensagem: 'Cadastro realizado com sucesso!',
      titulo: 'Bem-vindo!' 
    })
    router.push('/login')
  } catch (err) {
    toast.error({ mensagem: 'Erro ao criar conta. Tente novamente.' })
  }
}
</script>
```

### Uso em Requisições API

```typescript
<script setup lang="ts">
import { useToast } from '@/composables/useToast'

const toast = useToast()

async function salvarDados() {
  toast.info({ mensagem: 'Salvando dados...', titulo: 'Aguarde' })

  try {
    await api.post('/dados', dados)
    toast.success({ mensagem: 'Dados salvos com sucesso!' })
  } catch (err) {
    toast.error({ mensagem: 'Erro ao salvar dados' })
  }
}
</script>
```

## 🎨 Tipos Disponíveis

| Tipo | Cor | Ícone | Uso |
|------|-----|-------|-----|
| `success` | Verde | ✓ | Operações bem-sucedidas |
| `error` | Vermelho | ✗ | Erros e falhas |
| `warning` | Amarelo | ⚠ | Avisos e alertas |
| `info` | Azul | ℹ | Informações gerais |

## ⚙️ Opções Avançadas

### Parâmetros Disponíveis

Você pode usar **duas sintaxes**:

#### Sintaxe 1: String simples
```typescript
toast.success('Mensagem')  // Usa título padrão
toast.error('Mensagem')    // Usa título padrão "Erro!"
toast.warning('Mensagem')  // Usa título padrão "Atenção!"
toast.info('Mensagem')     // Sem título padrão
```

#### Sintaxe 2: Objeto com parâmetros nomeados
```typescript
toast.success({
  mensagem: string,    // ✅ Obrigatório
  titulo?: string,     // ❌ Opcional (usa padrão se não informado)
  duracao?: number     // ❌ Opcional (padrão: 5000ms)
})
```

**Vantagens da sintaxe com objeto:**
- ✅ Parâmetros em qualquer ordem
- ✅ Mais legível e explícito
- ✅ Fácil de adicionar/remover parâmetros

### Remover Toast Específico

```typescript
const toastId = toast.success({ mensagem: 'Mensagem' })
// Mais tarde...
toast.remove(toastId)
```

### Limpar Todos os Toasts

```typescript
toast.clear()
```

### Toast sem Auto-Close

```typescript
toast.warning({
  mensagem: 'Esta mensagem não fechará automaticamente',
  duracao: 0  // 0 = não fecha automaticamente
})
```

## 🎯 Melhores Práticas

1. **Use a sintaxe que fizer mais sentido**:
   - String simples para casos básicos
   - Objeto para casos com múltiplos parâmetros

2. **Escolha títulos descritivos** quando necessário:
   ```typescript
   // ❌ Evite
   toast.error({ mensagem: 'Erro', titulo: 'Erro' })
   
   // ✅ Prefira
   toast.error({ mensagem: 'Não foi possível salvar', titulo: 'Erro de conexão' })
   ```

3. **Mantenha mensagens curtas** e objetivas:
   ```typescript
   // ❌ Muito longo
   toast.success({ mensagem: 'O seu cadastro foi realizado com sucesso e você já pode fazer login no sistema usando suas credenciais' })
   
   // ✅ Conciso
   toast.success({ mensagem: 'Cadastro realizado com sucesso!' })
   ```

4. **Ajuste a duração** baseada na importância:
   ```typescript
   toast.success({ mensagem: 'Salvo!', duracao: 3000 })              // Sucesso rápido: 3s
   toast.error({ mensagem: 'Erro ao salvar', duracao: 7000 })        // Erro importante: 7s
   toast.warning({ mensagem: 'Atenção importante', duracao: 10000 }) // Aviso crítico: 10s
   ```

5. **Apenas um toast por vez**: O sistema já garante isso automaticamente

6. **Use o tipo apropriado** para cada situação:
   - ✅ `success` → Operações bem-sucedidas
   - ❌ `error` → Erros e falhas
   - ⚠️ `warning` → Avisos e validações
   - ℹ️ `info` → Informações gerais

## 🔧 Personalização

Para personalizar as cores ou estilos, edite:
- `components/Toast/index.vue` - Componente principal
- `composables/useToast.ts` - Lógica do composable

## 📱 Responsividade

O Toast é totalmente responsivo e se adapta a diferentes tamanhos de tela:
- Desktop: Canto superior direito
- Mobile: Topo da tela, largura ajustada
