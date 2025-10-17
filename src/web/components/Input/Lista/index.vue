<template>
  <div v-if="visivel" class="w-full" :class="clsx({'mb-4' : props.marginBottom})">
    <label v-if="props.label" class="mb-1 block font-medium text-grayScale-800">
      {{ props.label }}
    </label>
    <div class="relative">
      <!-- "Input" wrapper com cardzinhos dentro -->
      <div
        class="flex flex-wrap gap-2 w-full min-h-[42px] rounded-lg bg-input-100 border border-input-200 px-2.5 py-1.5 text-sm"
        :class="clsx({
          'cursor-not-allowed opacity-[0.40]': !habilitado,
          'ring-[0.0600rem] ring-[#ff3b3b]': hasError && !hasSuccess,
          'ring-[0.0600rem] ring-primary border-primary': isInputFocused,
          'ring-[0.0600rem] ring-primary rounded-b-none': isOpen && filteredResults.length > 0,
          'ring-[0.0600rem] ring-[#22bb33]': !hasError && hasSuccess && content,
        })"
        @click="focus"
      >

        <!-- Cards selecionados que ficam dentro do input -->
        <div
          v-for="(s, i) in selecionadosDescricoes"
          :key="`${s}-${i}`"
          @click.stop="removerSelecionado(i)"
          class="pl-2 pr-1.5 py-1.5 rounded-md bg-grayScale-100 border border-grayScale-400 font-semibold text-sm flex items-center gap-1 cursor-pointer duration-150 group hover:opacity-75 max-w-[300px] truncate"
        >
          <span class="truncate text-grayScale-800">{{ s }}</span>
          <div>
            <DesignV2IconHero name-icon="XMarkIcon" class="text-grayScale-600 w-5 h-5" />
          </div>
        </div>


        
        <!-- Campo de digitação (ocupa o espaço restante se tiver a largura mínima dele disponível de espaço) -->
        <input
          ref="inputRef"
          v-model="content"
          @input="results"
          @focus="handleInputFocus"
          @focusout="resetContent"
          @keydown.enter.prevent="$event.preventDefault()"
          @keydown.backspace="handleBackspace"
          @blur="handleInputBlur"
          :placeholder="props.placeholder ?? 'Buscar...'" 
          :disabled="!habilitado"
          autocomplete="off"
          class="block flex-1 min-w-[65px] bg-transparent outline-none focus:border-0 focus:ring-0 border-none text-sm text-grayScale-700"
        />
      </div>



    <!-- Dropdown de sugestões -->
    <Transition name="dropdown">
      <ul
        v-if="isOpen && filteredResults?.length > 0"
        class="absolute w-full left-0 top-full z-[999] max-h-[200px] overflow-y-auto rounded-lg border bg-input-100 border-input-200 mt-[1px]"
      >
        <li
          v-for="(opcao, index) in filteredResults"
          :key="opcao?.chave ?? opcao?.descricao ?? index"
          class="cursor-pointer border-b border-input-200 py-2 flex px-3 hover:bg-grayScale-300 last:border-0"
          @mousedown.prevent="selectContent(opcao)"
        >
          <span v-if="opcao && opcao.descricao" class="w-full flex-wrap text-sm text-grayScale-800">
            {{ opcao.descricao }}
          </span>
        </li>
      </ul>
    </Transition>

    </div>

    <span class="text-[#ff3b3b] text-sm">{{ props.errorMessage }}</span>
  </div>
</template>


<script setup lang="ts">
  import type { InputHTMLAttributes } from "vue";
  import { clsx } from "clsx";

  enum Placeholders {
    AUTOCOMPLETE = "Pesquisar",
    SELECT = "Selecionar",
  }
  type PlaceholderKeys = keyof typeof Placeholders;

  interface ItemModelo {
    descricao: string;
    chave?: any;
    [k: string]: any;
  }

  interface InputSelectAutocompleteProps {
    label?: string;
    hasSuccess?: boolean;
    hasError?: boolean;
    errorMessage?: string;
    habilitado?: boolean;
    type?: InputHTMLAttributes["type"];
    placeholder?: InputHTMLAttributes["placeholder"];
    placeholderType?: PlaceholderKeys;
    value?: string;
    valorPadrao?: any;
    maxLength?: number;
    model?: ItemModelo[];
    modelType?: "dynamic-list" | "static-list";
    visivel?: boolean;
    propriedade: any;
    informacoesAction?: any;
    valor?: any;
    obrigatorio?: boolean;
    tipoDeDado?: string;
    marginBottom?: boolean;
    automatico?: boolean;
  }

  const props = withDefaults(defineProps<InputSelectAutocompleteProps>(), {
    habilitado: true,
    visivel: true,
    obrigatorio: false,
    marginBottom: true
  });

  const emit = defineEmits<{
    (e: "emitValue", v: string): void;
    (e: "emitSelected", v: string[]): void;
  }>();

  const completeList = computed(() => props.model ?? []);

  const content = defineModel<string>(); // query atual
  defineExpose({ focus });

  const inputRef = ref();
  const isOpen = ref(false);
  const isInputFocused = ref(false);
  const resultNotFound = ref(false);

  const selecionadosChaves = ref<(string | number)[]>([]);
  const selecionadosDescricoes = ref<string[]>([]);

  const selecionaPlaceholder = () => {
    if (props.placeholderType) return Placeholders[props.placeholderType];
    return props.placeholder;
  };

  function focus() {
    inputRef.value?.focus();
  }

  const handleInputFocus = () => {
    isInputFocused.value = true;
    if (!isOpen.value && !valorSelecionado.value && content.value)
      showOptions();
  };

  const handleInputBlur = () => {
    isInputFocused.value = false;
    closeOptions();
  };

  const filteredResults = computed(() => {
    const lista = completeList.value ?? [];
    const q = (content.value ?? "").toLowerCase().trim();
    const setSel = new Set(selecionadosChaves.value);

    // Para tirar itens já selecionados na lista
    const baseSemSelecionados = lista.filter((i: ItemModelo) => {
      const chave = i?.chave ?? i?.descricao ?? String(i);
      return !setSel.has(chave);
    });

    // Espera o usuário parar de digitar (0,3s) e lança o content para o input de fato (útil para fazer requisição)
    if (props.modelType === "dynamic-list") {
      return baseSemSelecionados;
    }

    // Busca pelo texto que está sendo digitado com filtro no front
    return baseSemSelecionados.filter((i: ItemModelo) => {
      const desc = i?.descricao ?? String(i);
      return q ? desc.toLowerCase().includes(q) : true;
    });
  });

  const parouDeDigitar = ref(false);
  let timeoutId: any;

  async function results() {
    valorSelecionado.value = false;
    parouDeDigitar.value = false;
    resultNotFound.value = false;

    if (timeoutId) clearTimeout(timeoutId);

    if (props.modelType === "static-list") {
      emit("emitValue", content.value || "");
      if (content.value) {
        showOptions();
      } else {
        closeOptions();
      }
      return;
    }

    timeoutId = setTimeout(async () => {
      parouDeDigitar.value = true;
      emit("emitValue", content.value || "");
      if (content.value) {
        showOptions();
      } else {
        closeOptions();
      }
    }, 300);
  }


  const valorSelecionado = ref(false);

  function selectContent(item: ItemModelo) {
    const key = item?.chave ?? String(item);
    const label = item?.descricao ?? String(item);

    if (!selecionadosChaves.value.includes(key)) {
      selecionadosChaves.value.push(key);
      selecionadosDescricoes.value.push(label);
      emit("emitSelected", [...selecionadosChaves.value]);
    }

    content.value = "";
    valorSelecionado.value = true;
    closeOptions();
  }


  function removerSelecionado(index: number) {
    selecionadosChaves.value.splice(index, 1);
    selecionadosDescricoes.value.splice(index, 1);
    emit("emitSelected", [...selecionadosChaves.value]);
  }

  function closeOptions() {
    isOpen.value = false;
  }

  function showOptions() {
    isOpen.value = true;
  }

  function resetContent() {
    if (!valorSelecionado.value) {
      content.value = "";
    }
    valorSelecionado.value = false;
    parouDeDigitar.value = false;
    resultNotFound.value = false;
  }
  
  function normalizaValor(v: any): { keys: (string | number)[]; labels: string[] } {
    if (typeof v === "string") {
      const trimmed = v.trim();
      if (trimmed.startsWith("[") || trimmed.startsWith("{")) {
        try {
          v = JSON.parse(trimmed);
        } catch {
          return { keys: [trimmed], labels: [trimmed] };
        }
      } else {
        return { keys: [trimmed], labels: [trimmed] };
      }
    }

    const arr = Array.isArray(v) ? v : v ? [v] : [];

    const keys: (string | number)[] = [];
    const labels: string[] = [];

    for (const item of arr) {
      if (item && typeof item === "object") {
        const key = item.chave;
        const label = item.descricao;

        // se chave e descricao forem null → ignora
        if ((key === null || key === undefined) && (label === null || label === undefined)) {
          continue;
        }

        keys.push(key ?? "");
        labels.push(label ?? String(key ?? ""));
      } else {
        keys.push(item);
        labels.push(String(item));
      }
    }

    return { keys, labels };
  }

  onMounted(() => {
    const { keys, labels } = normalizaValor(props.valor);
    selecionadosChaves.value = keys;
    selecionadosDescricoes.value = labels;
    emit("emitSelected", [...selecionadosChaves.value]); // se só vier null → []
  });

  function handleBackspace(e: KeyboardEvent) {
    if (!content.value && selecionadosChaves.value.length > 0) {
      selecionadosChaves.value.pop();
      selecionadosDescricoes.value.pop();
      emit("emitSelected", [...selecionadosChaves.value]);
      e.preventDefault();
    }
  }

  watch(
  filteredResults,
    (newResults) => {
      if (newResults.length === 1 && isInputFocused.value && content.value == newResults[0].descricao && props.automatico) {
        selectContent(newResults[0]);
      }
    },
    { immediate: false }
  );
</script>


<style scoped>
  .scroll::-webkit-scrollbar {
    width: 7px;
    height: 3px;
  }

  .scroll::-webkit-scrollbar-thumb {
    background-color: #637788;
    border-radius: 10px;
  }

  /* no seu <style scoped> */
  .dropdown-enter-active,
  .dropdown-leave-active {
    transition: all 0.3s ease;
  }

  .dropdown-enter-from {
    opacity: 0;
    transform: translateY(-4px) scale(0.95);
    opacity: 0;
  }

  .dropdown-enter-to {
    opacity: 1;
    transform: translateY(0) scale(1);
    opacity: 1;

  }

  .dropdown-leave-from {
    opacity: 1;
    transform: translateY(0) scale(1);
  }

  .dropdown-leave-to {
    opacity: 0;
    transform: translateY(-4px) scale(0.95);
  }

</style>