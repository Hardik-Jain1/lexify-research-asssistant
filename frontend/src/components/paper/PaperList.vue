<!-- PaperList.vue -->
<template>
  <div class="space-y-4">
    <!-- Empty State -->
    <div v-if="!papers || papers.length === 0" class="relative overflow-hidden">
      <div class="absolute inset-0 bg-gradient-to-br from-slate-50 via-white to-indigo-50 opacity-60"></div>
      <div class="relative text-center py-16 bg-white/80 backdrop-blur-sm shadow-xl rounded-2xl border border-slate-200/60 p-8">
        <div class="relative">
          <div class="absolute inset-0 bg-gradient-to-r from-indigo-600/10 to-purple-600/10 rounded-full blur-3xl transform scale-150"></div>
          <div class="relative bg-gradient-to-br from-slate-100 to-slate-200 p-6 rounded-2xl w-24 h-24 mx-auto flex items-center justify-center shadow-inner">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-10 h-10 text-slate-500">
              <path stroke-linecap="round" stroke-linejoin="round" d="M19.5 14.25v-2.625a3.375 3.375 0 0 0-3.375-3.375h-1.5A1.125 1.125 0 0 1 13.5 7.125v-1.5a3.375 3.375 0 0 0-3.375-3.375H8.25m0 12.75h7.5m-7.5 3H12M10.5 2.25H5.625c-.621 0-1.125.504-1.125 1.125v17.25c0 .621.504 1.125 1.125 1.125h12.75c.621 0 1.125-.504 1.125-1.125V11.25a9 9 0 0 0-9-9Z" />
            </svg>
          </div>
        </div>
        <h3 class="mt-6 text-xl font-semibold text-slate-700">No research papers found</h3>
        <p class="mt-2 text-slate-500 max-w-sm mx-auto">Try adjusting your search criteria or explore different keywords to discover relevant papers.</p>
        <div class="mt-6 flex justify-center">
          <div class="inline-flex items-center px-4 py-2 rounded-full bg-indigo-50 text-indigo-600 text-sm font-medium">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-4 h-4 mr-2">
              <path stroke-linecap="round" stroke-linejoin="round" d="m21 21-5.197-5.197m0 0A7.5 7.5 0 1 0 5.196 5.196a7.5 7.5 0 0 0 10.607 10.607Z" />
            </svg>
            Refine your search
          </div>
        </div>
      </div>
    </div>

    <!-- Papers Grid -->
    <div class="space-y-3">
      <div
        v-for="paper in papers"
        :key="paper.db_id"
        :id="`paper-item-${paper.db_id}`"
        class="group relative bg-white/90 backdrop-blur-sm border border-slate-200/60 rounded-2xl shadow-lg hover:shadow-2xl transition-all duration-300 ease-out hover:-translate-y-1"
        :class="{ 
          'ring-2 ring-indigo-500/30 border-indigo-300 shadow-indigo-100': paper.is_selected_for_chat,
          'hover:border-slate-300/80': !paper.is_selected_for_chat
        }"
      >
        <!-- Selected Paper Indicator -->
        <div 
          v-if="paper.is_selected_for_chat" 
          class="absolute -left-1 top-6 bottom-6 w-1 bg-gradient-to-b from-indigo-500 to-purple-600 rounded-r-full shadow-lg"
        ></div>
        
        <!-- Subtle Background Pattern -->
        <div class="absolute inset-0 bg-gradient-to-br from-slate-50/50 via-transparent to-indigo-50/30 rounded-2xl"></div>
        
        <div class="relative">
          <PaperItem
            :paper="paper"
            @update-paper-selection="handlePaperSelectionUpdate"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { defineProps, defineEmits } from 'vue';
import PaperItem from './PaperItem.vue';
import type { Paper } from '@/types';

const props = defineProps<{
  papers: Paper[];
}>();

const emit = defineEmits(['update-paper-selection']);

const handlePaperSelectionUpdate = (payload: { paperId: number, selected: boolean }) => {
  emit('update-paper-selection', payload);
};
</script>