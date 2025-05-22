<template>
  <div class="space-y-6">
    <div v-if="!papers || papers.length === 0" class="text-center py-10">
      <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-16 h-16 mx-auto text-gray-400">
        <path stroke-linecap="round" stroke-linejoin="round" d="M20.25 7.5l-.625 10.632a2.25 2.25 0 01-2.247 2.118H6.622a2.25 2.25 0 01-2.247-2.118L3.75 7.5M10 11.25h4M3.375 7.5h17.25c.621 0 1.125-.504 1.125-1.125V6.375c0-.621-.504-1.125-1.125-1.125H3.375c-.621 0-1.125.504-1.125 1.125v.001c0 .621.504 1.125 1.125 1.125z" />
      </svg>
      <p class="mt-4 text-lg text-gray-500">No papers to display.</p>
      <p class="text-sm text-gray-400">Try refining your search query.</p>
    </div>
    <PaperItem
      v-for="paper in papers"
      :key="paper.db_id"
      :paper="paper"
      @update-paper-selection="handlePaperSelectionUpdate" 
    />
    </div>
</template>

<script setup lang="ts">
import { defineProps, defineEmits } from 'vue'; // Added defineEmits
import PaperItem from './PaperItem.vue';
import type { Paper } from '@/types';

const props = defineProps<{
  papers: Paper[];
}>();

const emit = defineEmits(['update-paper-selection']); // Define the emit

const handlePaperSelectionUpdate = (payload: { paperId: number, selected: boolean }) => {
  // console.log('Paper selection update in PaperList, re-emitting:', payload); // For debugging
  emit('update-paper-selection', payload); // Re-emit to ResearchView
};
</script>