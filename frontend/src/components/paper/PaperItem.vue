<!-- PaperItem.vue -->
<template>
  <div class="p-6">
    <!-- Header Section -->
    <div class="flex justify-between items-start mb-4 gap-4">
      <div class="flex-1 min-w-0">
        <h3 class="text-lg sm:text-xl font-bold text-slate-800 hover:text-indigo-700 transition-colors duration-200 leading-tight">
          <a 
            :href="paper.pdf_url" 
            target="_blank" 
            rel="noopener noreferrer" 
            class="hover:underline decoration-2 decoration-indigo-300 underline-offset-2" 
            :title="`Open PDF: ${paper.title}`"
          >
            {{ paper.title }}
          </a>
        </h3>
      </div>
      
      <!-- Enhanced Checkbox -->
      <div class="flex-shrink-0">
        <div class="relative group">
          <input
            type="checkbox"
            :id="'select-paper-' + paper.db_id"
            :value="paper.db_id"
            v-model="localIsSelected" 
            @change="toggleSelection" 
            :disabled="!paper.is_processed_for_chat"
            class="sr-only"
          />
          <label 
            :for="'select-paper-' + paper.db_id" 
            class="relative flex items-center justify-center w-6 h-6 rounded-lg border-2 cursor-pointer transition-all duration-200"
            :class="[
              localIsSelected 
                ? 'bg-gradient-to-br from-indigo-500 to-purple-600 border-indigo-500 shadow-lg shadow-indigo-200' 
                : 'bg-white border-slate-300 hover:border-indigo-400 hover:shadow-md',
              !paper.is_processed_for_chat ? 'opacity-50 cursor-not-allowed' : 'group-hover:scale-110'
            ]"
            :title="paper.is_processed_for_chat ? 'Select for chat' : 'Paper not yet processed for chat'"
          >
            <svg 
              v-if="localIsSelected" 
              xmlns="http://www.w3.org/2000/svg" 
              viewBox="0 0 24 24" 
              fill="currentColor" 
              class="w-4 h-4 text-white"
            >
              <path fill-rule="evenodd" d="M19.916 4.626a.75.75 0 0 1 .208 1.04l-9 13.5a.75.75 0 0 1-1.154.114l-6-6a.75.75 0 0 1 1.06-1.06l5.353 5.353 8.493-12.74a.75.75 0 0 1 1.04-.207Z" clip-rule="evenodd" />
            </svg>
          </label>
        </div>
      </div>
    </div>

    <!-- Metadata Section -->
    <div class="space-y-2 mb-5">
      <div class="flex flex-wrap items-center gap-x-4 gap-y-1 text-sm">
        <div class="flex items-center text-slate-600">
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-4 h-4 mr-2 text-slate-400">
            <path stroke-linecap="round" stroke-linejoin="round" d="M15.75 6a3.75 3.75 0 1 1-7.5 0 3.75 3.75 0 0 1 7.5 0ZM4.501 20.118a7.5 7.5 0 0 1 14.998 0A17.933 17.933 0 0 1 12 21.75c-2.676 0-5.216-.584-7.499-1.632Z" />
          </svg>
          <span class="font-medium text-slate-700">Authors:</span>
          <span class="ml-1 text-slate-600">{{ paper.authors.join(', ') }}</span>
        </div>
      </div>
      
      <div class="flex flex-wrap items-center gap-x-4 gap-y-1 text-sm">
        <div class="flex items-center text-slate-600">
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-4 h-4 mr-2 text-slate-400">
            <path stroke-linecap="round" stroke-linejoin="round" d="M6.75 3v2.25M17.25 3v2.25M3 18.75V7.5a2.25 2.25 0 0 1 2.25-2.25h13.5A2.25 2.25 0 0 1 21 7.5v11.25m-18 0A2.25 2.25 0 0 0 5.25 21h13.5A2.25 2.25 0 0 0 21 18.75m-18 0v-7.5A2.25 2.25 0 0 1 5.25 9h13.5A2.25 2.25 0 0 1 21 11.25v7.5" />
          </svg>
          <span class="font-medium text-slate-700">Published:</span>
          <span class="ml-1 text-slate-600">{{ paper.published }}</span>
        </div>
        
        <div class="flex items-center text-slate-600">
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-4 h-4 mr-2 text-slate-400">
            <path stroke-linecap="round" stroke-linejoin="round" d="M5.25 8.25h15m-16.5 7.5h15m-1.6-13.5 2.3 2.3-2.3 2.3m-13.4 0L4.25 9.75l2.3-2.3" />
          </svg>
          <span class="font-medium text-slate-700">ID:</span>
          <span class="ml-1 font-mono text-slate-600">{{ paper.paper_id }}</span>
        </div>
      </div>
    </div>

    <!-- Summary Section -->
    <div v-if="paper.individual_summary" class="mb-5 relative overflow-hidden">
      <div class="absolute inset-0 bg-gradient-to-br from-indigo-50 to-purple-50 rounded-xl"></div>
      <div class="relative p-4 border border-indigo-200/60 rounded-xl backdrop-blur-sm">
        <div class="flex items-center mb-3">
          <div class="w-2 h-2 bg-gradient-to-r from-indigo-500 to-purple-500 rounded-full mr-3"></div>
          <h4 class="text-sm font-bold text-indigo-900">AI Summary</h4>
        </div>
        <p class="text-sm text-slate-700 leading-relaxed whitespace-pre-line">
          {{ paper.individual_summary }}
        </p>
      </div>
    </div>

    <!-- Abstract Section -->
    <div v-if="paper.abstract && !paper.individual_summary" class="mb-5 relative overflow-hidden">
      <div class="absolute inset-0 bg-gradient-to-br from-slate-50 to-slate-100 rounded-xl"></div>
      <div class="relative p-4 border border-slate-200/60 rounded-xl backdrop-blur-sm">
        <div class="flex items-center mb-3">
          <div class="w-2 h-2 bg-slate-400 rounded-full mr-3"></div>
          <h4 class="text-sm font-bold text-slate-700">Abstract</h4>
        </div>
        <p class="text-sm text-slate-700 leading-relaxed whitespace-pre-line">
          {{ paper.abstract }}
        </p>
      </div>
    </div>

    <!-- Footer Actions -->
    <div class="flex items-center justify-between pt-4 border-t border-slate-100">
      <div class="flex items-center">
        <span
          :class="[
            'inline-flex items-center px-3 py-1.5 rounded-full font-semibold text-xs transition-all duration-200',
            paper.is_processed_for_chat 
              ? 'bg-gradient-to-r from-emerald-100 to-green-100 text-emerald-700 border border-emerald-200/60 shadow-sm' 
              : 'bg-gradient-to-r from-amber-100 to-yellow-100 text-amber-700 border border-amber-200/60 shadow-sm animate-pulse'
          ]"
        >
          <div 
            :class="[
              'w-2 h-2 rounded-full mr-2',
              paper.is_processed_for_chat ? 'bg-emerald-500' : 'bg-amber-500'
            ]"
          ></div>
          {{ paper.processing_status_message || (paper.is_processed_for_chat ? 'Ready for Chat' : 'Processing...') }}
        </span>
      </div>

      <a
        :href="paper.pdf_url"
        target="_blank"
        rel="noopener noreferrer"
        class="group inline-flex items-center px-4 py-2 text-sm font-medium text-indigo-600 hover:text-indigo-700 hover:bg-indigo-50 rounded-lg transition-all duration-200"
        title="View PDF"
      >
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-4 h-4 mr-2 group-hover:scale-110 transition-transform duration-200">
          <path stroke-linecap="round" stroke-linejoin="round" d="M19.5 14.25v-2.625a3.375 3.375 0 0 0-3.375-3.375h-1.5A1.125 1.125 0 0 1 13.5 7.125v-1.5a3.375 3.375 0 0 0-3.375-3.375H8.25m2.25 0H5.625c-.621 0-1.125.504-1.125 1.125v17.25c0 .621.504 1.125 1.125 1.125h12.75c.621 0 1.125-.504 1.125-1.125V11.25a9 9 0 0 0-9-9Z" />
        </svg>
        View PDF
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

const emit = defineEmits(['update-paper-selection']);

const localIsSelected = ref(props.paper.is_selected_for_chat || false);

watch(() => props.paper.is_selected_for_chat, (newValue) => {
  localIsSelected.value = newValue || false;
});

const toggleSelection = () => {
  emit('update-paper-selection', { paperId: props.paper.db_id, selected: localIsSelected.value });
};
</script>