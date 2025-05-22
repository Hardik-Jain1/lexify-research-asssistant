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
      @update:selectedPapers="handlePaperSelectionUpdate" 
    />
    </div>
</template>

<script setup lang="ts">
import { defineProps } from 'vue';
import PaperItem from './PaperItem.vue';
import type { Paper } from '@/types';

const props = defineProps<{
  papers: Paper[];
}>();

// This component currently just displays. Selection state will be managed higher up.
const handlePaperSelectionUpdate = (payload: { paperId: number, selected: boolean }) => {
  // This is a placeholder. The actual logic for managing a list of selected paper IDs
  // will live in ResearchView.vue or a dedicated Pinia store.
  // PaperList.vue might not need to handle this event directly if ResearchView.vue
  // passes down a method to PaperItem.vue or manages selected state through props.
  console.log('Paper selection update in PaperList:', payload);
};
</script>