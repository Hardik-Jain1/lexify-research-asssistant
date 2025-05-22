<template>
  <div class="space-y-8">
    <div class="p-6 bg-white shadow-xl rounded-lg">
      <h1 class="text-3xl font-bold text-gray-800 mb-6 text-center">AI Research Assistant</h1>
      
      <form @submit.prevent="handleSearch" class="flex flex-col sm:flex-row gap-4 mb-8">
        <input
          type="text"
          v-model="searchQuery"
          placeholder="Enter your research query (e.g., 'transformer models for NLP')"
          required
          class="flex-grow appearance-none rounded-lg relative block w-full px-4 py-3 border border-gray-300 placeholder-gray-500 text-gray-900 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
        />
        <button
          type="submit"
          :disabled="isLoadingSearch"
          class="inline-flex items-center justify-center px-6 py-3 border border-transparent text-base font-medium rounded-lg shadow-sm text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:bg-indigo-400 disabled:cursor-not-allowed"
        >
          <svg v-if="isLoadingSearch" class="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
          {{ isLoadingSearch ? 'Searching...' : 'Search Papers' }}
        </button>
      </form>

      <div v-if="searchError" class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded-md relative mb-6" role="alert">
        <strong class="font-bold">Search Error: </strong>
        <span class="block sm:inline">{{ searchError }}</span>
      </div>
    </div>

    <div v-if="isLoadingSearch && !processedPapers.length" class="text-center py-10">
      <div class="inline-block animate-spin rounded-full h-12 w-12 border-t-4 border-b-4 border-indigo-600"></div>
      <p class="mt-4 text-lg text-gray-600">Fetching research papers...</p>
    </div>
    
    <div v-if="searchResults" class="space-y-8">
      <!-- Consolidated Summary Display -->
      <div v-if="searchResults.consolidated_summary" class="p-6 bg-indigo-50 rounded-lg shadow border border-indigo-200">
        <h2 class="text-xl font-semibold text-indigo-800 mb-3">Consolidated Summary</h2>
        <p class="text-gray-700 leading-relaxed whitespace-pre-line">{{ searchResults.consolidated_summary }}</p>
      </div>
      
      <div class="p-6 bg-white shadow-lg rounded-lg">
        <div class="flex flex-col md:flex-row justify-between md:items-center mb-4">
            <h2 class="text-2xl font-semibold text-gray-700">
              Found Papers ({{ processedPapers.length }})
            </h2>
            <div v-if="selectedPapersForChat.size > 0" class="mt-2 md:mt-0">
                <button @click="startChatting" 
                        class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-green-600 hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500">
                    Chat with {{ selectedPapersForChat.size }} Selected Paper(s)
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" class="w-5 h-5 ml-2">
                        <path d="M10 3a.75.75 0 01.75.75v1.5h1.5a.75.75 0 010 1.5h-1.5v1.5a.75.75 0 01-1.5 0v-1.5h-1.5a.75.75 0 010-1.5h1.5v-1.5A.75.75 0 0110 3zM3.055 7.278a.75.75 0 00-1.06 1.06l1.25 1.25a.75.75 0 001.06 0l1.25-1.25a.75.75 0 00-1.06-1.06L4 7.94l-.22-.223a.75.75 0 00-1.061-.06zM3.5 11.75a.75.75 0 00-1.5 0v1.5c0 .621.504 1.125 1.125 1.125h1.25a.75.75 0 000-1.5H3.5v-1.5zM10 17a.75.75 0 01-.75-.75v-1.5h-1.5a.75.75 0 010-1.5h1.5v-1.5a.75.75 0 011.5 0v1.5h1.5a.75.75 0 010 1.5h-1.5v1.5A.75.75 0 0110 17zM16.945 7.278a.75.75 0 00-1.06-1.06l-1.25 1.25a.75.75 0 001.06 1.06l1.25-1.25a.75.75 0 00-.22-.723.75.75 0 00-.84-.039zm0 4.472a.75.75 0 00-1.5 0v1.5c0 .621.504 1.125 1.125 1.125h1.25a.75.75 0 000-1.5h-1.25v-1.5z" />
                    </svg>
                </button>
            </div>
        </div>
        <PaperList :papers="processedPapers" @update-paper-selection="updateSelectedPapers" />
      </div>
    </div>
     <div v-else-if="!isLoadingSearch && !searchQuerySubmitted" class="text-center text-gray-500 py-10 bg-white shadow-lg rounded-lg p-6">
      Enter a query above and click "Search Papers" to begin.
    </div>

    <div v-if="isChatting" class="fixed inset-0 bg-gray-800 bg-opacity-75 flex items-center justify-center z-50 p-4">
        <div class="bg-white p-6 rounded-lg shadow-xl w-full max-w-3xl h-[80vh] flex flex-col">
            <h3 class="text-xl font-semibold mb-4">Chatting with Selected Papers</h3>
            <div class="flex-grow overflow-y-auto mb-4 border p-2 rounded-md">
                <!-- ChatInterface.vue will go here -->
                Chat messages placeholder...
            </div>
            <input type="text" placeholder="Ask a question..." class="w-full p-2 border rounded-md">
            <button @click="isChatting = false" class="mt-4 bg-red-500 text-white px-4 py-2 rounded-md hover:bg-red-600">Close Chat</button>
        </div>
    </div>

  </div>
</template>

<script setup lang="ts">
import { ref, onBeforeUnmount, watch } from 'vue';
import * as paperService from '@/services/paperService';
import type { Paper, PaperSearchResponse, PaperStatusResponse } from '@/types';
import PaperList from '@/components/paper/PaperList.vue';

const searchQuery = ref('');
const isLoadingSearch = ref(false);
const searchError = ref<string | null>(null);
const searchResults = ref<PaperSearchResponse | null>(null);
const searchQuerySubmitted = ref(false);

const processedPapers = ref<Paper[]>([]);
const selectedPapersForChat = ref<Set<number>>(new Set());
const isChatting = ref(false);

const pollingIntervals = ref<Map<number, ReturnType<typeof setInterval>>>(new Map());

const POLLING_INTERVAL_MS = 7000; 
const MAX_POLLING_ATTEMPTS_BEFORE_RETRY = 5; 

const clearAllPollingIntervals = () => {
  pollingIntervals.value.forEach(intervalId => clearInterval(intervalId));
  pollingIntervals.value.clear();
};

onBeforeUnmount(() => {
  clearAllPollingIntervals();
});

const fetchAndUpdatePaperStatus = async (paperDbId: number) => {
  try {
    const statusResponse = await paperService.getPaperStatus(paperDbId);
    const paperToUpdate = processedPapers.value.find(p => p.db_id === paperDbId);

    if (paperToUpdate) {
      paperToUpdate.is_processed_for_chat = statusResponse.is_ready_for_chat;

      if (statusResponse.is_ready_for_chat) {
        paperToUpdate.processing_status_message = 'Ready for Chat';
        paperToUpdate.is_polling_status = false;
        paperToUpdate.retryInitiated = false; 
        const intervalId = pollingIntervals.value.get(paperDbId);
        if (intervalId) {
          clearInterval(intervalId);
          pollingIntervals.value.delete(paperDbId);
        }
      } else {
        paperToUpdate.pollingAttempts = (paperToUpdate.pollingAttempts || 0) + 1;

        // Set status message based on current state
        if (statusResponse.processing_status_notes && statusResponse.processing_status_notes !== 'arXiv' && statusResponse.processing_status_notes.match(/Failed|Error/i)) {
          paperToUpdate.processing_status_message = statusResponse.processing_status_notes;
        } else if (paperToUpdate.retryInitiated && !paperToUpdate.processing_status_message?.startsWith('Retry failed:')) {
           paperToUpdate.processing_status_message = 'Processing... (after retry attempt)';
        } else if (!paperToUpdate.retryInitiated) { 
          paperToUpdate.processing_status_message = 'Processing...';
        }
        // If already "Retry failed:", keep that message unless a new status comes.

        // Retry logic
        if (paperToUpdate.pollingAttempts >= MAX_POLLING_ATTEMPTS_BEFORE_RETRY && 
            !paperToUpdate.retryInitiated && 
            paperToUpdate.is_polling_status) {
          
          paperToUpdate.retryInitiated = true; 
          paperToUpdate.processing_status_message = 'Retrying processing...'; 
          
          console.log(`Attempting to manually re-process paper ${paperDbId} after ${paperToUpdate.pollingAttempts} attempts.`);
          try {
            await paperService.retryProcessPaper(paperDbId);
            console.log(`Manual processing re-initiated for paper ${paperDbId}.`);
            paperToUpdate.pollingAttempts = 0; // Reset attempts for the new processing cycle
          } catch (retryError: any) {
            console.error(`Failed to trigger retry for paper ${paperDbId}:`, retryError);
            paperToUpdate.processing_status_message = `Retry failed: ${retryError.response?.data?.msg || retryError.message || 'Unknown error'}`;
            // Keep retryInitiated = true to prevent immediate auto-retries by this logic block.
            // Polling continues, and if the backend resolves it, status will update.
            // If backend fails again, processing_status_notes might show a new error.
          }
        }
      }
    } else {
      const intervalId = pollingIntervals.value.get(paperDbId);
      if (intervalId) {
        clearInterval(intervalId);
        pollingIntervals.value.delete(paperDbId);
      }
    }
  } catch (error: any) {
    console.error(`Failed to get status for paper ${paperDbId}:`, error);
    const paperToUpdate = processedPapers.value.find(p => p.db_id === paperDbId);
    if (paperToUpdate) {
      // Avoid overwriting a more specific "Retry failed:" message with a generic "Error fetching status"
      if (!paperToUpdate.processing_status_message?.startsWith('Retry failed:')) {
        paperToUpdate.processing_status_message = `Error fetching status: ${error.response?.data?.msg || error.message || 'Unknown error'}`;
      }
    }
  }
};

const pollPaperStatus = (paperDbId: number) => {
  if (pollingIntervals.value.has(paperDbId)) {
    return; 
  }

  const paper = processedPapers.value.find(p => p.db_id === paperDbId);
  if (paper && paper.is_polling_status && !paper.is_processed_for_chat) {
    fetchAndUpdatePaperStatus(paperDbId).then(() => {
      const updatedPaper = processedPapers.value.find(p => p.db_id === paperDbId);
      if (updatedPaper && updatedPaper.is_polling_status && !updatedPaper.is_processed_for_chat) {
        const intervalId = setInterval(() => fetchAndUpdatePaperStatus(paperDbId), POLLING_INTERVAL_MS);
        pollingIntervals.value.set(paperDbId, intervalId);
      }
    });
  }
};

const startPollingForUnprocessedPapers = () => {
  processedPapers.value.forEach(paper => {
    if (paper.is_polling_status && !paper.is_processed_for_chat) {
      pollPaperStatus(paper.db_id);
    }
  });
};

const handleSearch = async () => {
  if (!searchQuery.value.trim()) {
    searchError.value = 'Please enter a search query.';
    return;
  }
  isLoadingSearch.value = true;
  searchError.value = null;
  searchResults.value = null;
  searchQuerySubmitted.value = true; 
  
  clearAllPollingIntervals(); 
  processedPapers.value = [];
  selectedPapersForChat.value.clear();
  isChatting.value = false;

  try {
    const response = await paperService.searchPapers(searchQuery.value);
    searchResults.value = response;
    processedPapers.value = response.papers.map(p => ({
      ...p,
      processing_status_message: p.is_processed_for_chat 
        ? 'Ready for Chat' 
        : (p.source && p.source !== 'arXiv' && p.source.match(/Failed|Error/i) 
            ? p.source 
            : 'Processing...'), 
      is_polling_status: !p.is_processed_for_chat,
      is_selected_for_chat: false, 
      pollingAttempts: 0,
      retryInitiated: false,
    }));
    startPollingForUnprocessedPapers();
  } catch (error: any) {
    console.error('Search failed:', error);
    searchError.value = error.response?.data?.msg || error.message || 'Failed to fetch papers. Please try again.';
    searchResults.value = null; 
    processedPapers.value = []; 
  } finally {
    isLoadingSearch.value = false;
  }
};

const updateSelectedPapers = (payload: { paperId: number, selected: boolean }) => {
  const paper = processedPapers.value.find(p => p.db_id === payload.paperId);
  if (paper) {
    paper.is_selected_for_chat = payload.selected; 
    if (payload.selected) {
      selectedPapersForChat.value.add(payload.paperId);
    } else {
      selectedPapersForChat.value.delete(payload.paperId);
    }
  }
};

const startChatting = () => {
  if (selectedPapersForChat.value.size > 0) {
    const papersToChat = processedPapers.value.filter(p => selectedPapersForChat.value.has(p.db_id));
    const allSelectedAreReady = papersToChat.every(p => p.is_processed_for_chat);

    if (!allSelectedAreReady) {
      alert('Some selected papers are not yet ready for chat. Please wait for processing to complete or unselect them.');
      return;
    }
    console.log('Start chatting with papers:', Array.from(selectedPapersForChat.value));
    isChatting.value = true;
  } else {
    alert('Please select at least one paper that is ready for chat.');
  }
};

watch(selectedPapersForChat, (newSelection) => {
  // console.log('Selected papers changed:', newSelection);
}, { deep: true });

</script>

<style scoped>
.whitespace-pre-line {
  white-space: pre-line;
}
</style>