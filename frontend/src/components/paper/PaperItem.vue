<template>
  <div class="p-5 border border-gray-200 rounded-lg shadow-sm hover:shadow-md transition-shadow duration-200 bg-white">
    <div class="flex justify-between items-start mb-2">
      <h3 class="text-xl font-semibold text-indigo-700 pr-4">
        <a :href="paper.pdf_url" target="_blank" rel="noopener noreferrer" class="hover:underline" :title="`Open PDF: ${paper.title}`">
          {{ paper.title }}
        </a>
      </h3>
      <div class="flex-shrink-0 ml-4">
        <input
          type="checkbox"
          :id="'select-paper-' + paper.db_id"
          :value="paper.db_id"
          v-model="localIsSelected" @change="toggleSelection" :disabled="!paper.is_processed_for_chat"
          class="h-5 w-5 text-indigo-600 border-gray-300 rounded focus:ring-indigo-500 disabled:opacity-50 disabled:cursor-not-allowed"
          :title="paper.is_processed_for_chat ? 'Select for chat' : 'Paper not yet processed for chat'"
        />
        <label :for="'select-paper-' + paper.db_id" class="sr-only">Select paper {{ paper.paper_id }}</label>
      </div>
    </div>

    <p class="text-xs text-gray-500 mb-1">
      <span class="font-medium">Authors:</span> {{ paper.authors.join(', ') }}
    </p>
    <p class="text-xs text-gray-500 mb-3">
      <span class="font-medium">Published:</span> {{ paper.published }} | <span class="font-medium">ID:</span> {{ paper.paper_id }}
    </p>

    <div v-if="paper.individual_summary" class="mb-3 p-3 bg-indigo-50 rounded-md border border-indigo-200">
      <h4 class="text-sm font-semibold text-indigo-800 mb-1">Summary:</h4>
      <p class="text-sm text-gray-700 leading-relaxed whitespace-pre-line">
        {{ paper.individual_summary }}
      </p>
    </div>
    
    <div v-if="paper.abstract && !paper.individual_summary" class="mb-3 p-3 bg-gray-50 rounded-md border border-gray-200">
      <h4 class="text-sm font-semibold text-gray-600 mb-1">Abstract:</h4>
      <p class="text-sm text-gray-700 leading-relaxed whitespace-pre-line">
        {{ paper.abstract }}
      </p>
    </div>

    <div class="mt-3 text-xs">
      <span
        :class="[
          'px-2.5 py-1 rounded-full font-medium',
          paper.is_processed_for_chat ? 'bg-green-100 text-green-800' : 'bg-yellow-100 text-yellow-800 animate-pulse'
        ]"
      >
        {{ paper.processing_status_message || (paper.is_processed_for_chat ? 'Ready for Chat' : 'Processing...') }}
      </span>
       <a 
        :href="paper.pdf_url" 
        target="_blank" 
        rel="noopener noreferrer" 
        class="ml-3 inline-flex items-center text-indigo-600 hover:text-indigo-800 hover:underline"
        title="Download PDF"
      >
        View PDF
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" class="w-4 h-4 ml-1">
          <path fill-rule="evenodd" d="M4.25 5.5a.75.75 0 000 1.5h5.5a.75.75 0 000-1.5h-5.5zm0 3a.75.75 0 000 1.5h3.5a.75.75 0 000-1.5h-3.5zm0 3a.75.75 0 000 1.5h5.5a.75.75 0 000-1.5h-5.5zm8-5a.75.75 0 01.75.75v4.5a.75.75 0 01-1.5 0v-4.5a.75.75 0 01.75-.75zm.75 8.25a.75.75 0 01-.75.75h-5.5a.75.75 0 010-1.5h5.5a.75.75 0 01.75.75z" clip-rule="evenodd" />
          <path d="M2 2.5A2.5 2.5 0 014.5 0h8.75a.75.75 0 01.75.75v3.5a.75.75 0 01-1.5 0V1.5H4.5a1 1 0 00-1 1V14a1 1 0 001 1h5.25a.75.75 0 010 1.5H4.5A2.5 2.5 0 012 14V2.5z" />
        </svg>
      </a>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch, defineProps, defineEmits } from 'vue';
import type { Paper } from '@/types';

const props = defineProps<{
  paper: Paper;
}>();

const emit = defineEmits(['updatePaperSelection']); // Changed emit name for clarity

const localIsSelected = ref(props.paper.is_selected_for_chat || false);

watch(() => props.paper.is_selected_for_chat, (newValue) => {
  // This watch ensures the checkbox reflects changes if the prop is updated from parent
  localIsSelected.value = newValue || false;
});

const toggleSelection = () => {
  // When the checkbox is clicked, its v-model (localIsSelected) updates.
  // Then, we emit this change to the parent.
  emit('updatePaperSelection', { paperId: props.paper.db_id, selected: localIsSelected.value });
};
</script>