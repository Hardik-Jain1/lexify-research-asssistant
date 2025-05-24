<template>
  <div class="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-50">
    <!-- Hero Section with Search -->
    <div class="relative overflow-hidden">
      <!-- Background decoration -->
      <div class="absolute inset-0 bg-gradient-to-r from-blue-600/5 to-indigo-600/5"></div>
      <div class="absolute top-0 right-0 w-96 h-96 bg-gradient-to-bl from-blue-400/10 to-transparent rounded-full blur-3xl"></div>
      <div class="absolute bottom-0 left-0 w-80 h-80 bg-gradient-to-tr from-indigo-400/10 to-transparent rounded-full blur-3xl"></div>
      
      <div class="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12 lg:py-20">
        <div class="text-center mb-12">
          <div class="inline-flex items-center justify-center w-16 h-16 bg-gradient-to-r from-blue-600 to-indigo-600 rounded-2xl mb-6 shadow-lg">
            <svg class="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
            </svg>
          </div>
            <h1 class="text-4xl lg:text-6xl font-bold bg-gradient-to-r from-slate-900 via-blue-900 to-indigo-900 bg-clip-text text-transparent mb-4">
            <span class="text-blue-600">Lexify</span>
            </h1>
            <p class="text-xl lg:text-2xl text-slate-600 font-light max-w-3xl mx-auto leading-relaxed">
            Your intelligent research companion for discovering and analyzing academic papers
            </p>
        </div>

        <!-- Enhanced Search Bar -->
        <div class="max-w-4xl mx-auto">
          <form @submit.prevent="handleSearch" class="relative group">
            <div class="relative">
              <div class="absolute inset-0 bg-gradient-to-r from-blue-600 to-indigo-600 rounded-2xl blur opacity-25 group-hover:opacity-40 transition-opacity duration-300"></div>
              <div class="relative bg-white/80 backdrop-blur-xl border border-white/60 rounded-2xl shadow-2xl overflow-hidden">
                <div class="flex items-center">
                  <div class="flex-1 relative">
                    <svg class="absolute left-6 top-1/2 transform -translate-y-1/2 w-6 h-6 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path>
                    </svg>
                    <input
                      type="text"
                      v-model="searchQuery"
                      placeholder="Enter your research query (e.g., 'transformer models for NLP')"
                      required
                      class="w-full pl-16 pr-6 py-6 text-lg bg-transparent text-slate-900 placeholder-slate-500 focus:outline-none"
                    />
                  </div>
                  <button
                    type="submit"
                    :disabled="isLoadingSearch"
                    class="m-2 px-8 py-4 bg-gradient-to-r from-blue-600 to-indigo-600 text-white font-semibold rounded-xl shadow-lg hover:from-blue-700 hover:to-indigo-700 focus:outline-none focus:ring-4 focus:ring-blue-500/50 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-200 transform hover:scale-105 active:scale-95"
                  >
                    <div class="flex items-center space-x-3">
                      <svg v-if="isLoadingSearch" class="animate-spin w-5 h-5" fill="none" viewBox="0 0 24 24">
                        <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                        <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                      </svg>
                      <svg v-else class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path>
                      </svg>
                      <span>{{ isLoadingSearch ? 'Searching...' : 'Search Papers' }}</span>
                    </div>
                  </button>
                </div>
              </div>
            </div>
          </form>

          <!-- Search Error -->
          <div v-if="searchError" class="mt-6 p-4 bg-red-50/80 backdrop-blur-sm border border-red-200 text-red-700 rounded-xl shadow-sm" role="alert">
            <div class="flex items-center">
              <svg class="w-5 h-5 mr-3 text-red-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
              </svg>
              <div>
                <strong class="font-semibold">Search Error: </strong>
                <span>{{ searchError }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="isLoadingSearch && !processedPapers.length" class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
      <div class="text-center">
        <div class="relative inline-block">
          <div class="w-16 h-16 border-4 border-blue-200 border-t-blue-600 rounded-full animate-spin"></div>
          <div class="absolute inset-0 w-16 h-16 border-4 border-transparent border-r-indigo-600 rounded-full animate-spin" style="animation-delay: -0.5s"></div>
        </div>
        <p class="mt-6 text-xl text-slate-600 font-medium">Discovering research papers...</p>
        <p class="mt-2 text-slate-500">This may take a few moments</p>
      </div>
    </div>
    
    <!-- Results Section -->
    <div v-if="searchResults" class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pb-20">
      <div class="space-y-8">
        <!-- Consolidated Summary -->
        <div v-if="searchResults.consolidated_summary" class="group">
          <div class="relative">
            <div class="absolute inset-0 bg-gradient-to-r from-emerald-500/10 to-teal-500/10 rounded-3xl blur-xl opacity-70 group-hover:opacity-100 transition-opacity duration-300"></div>
            <div class="relative bg-white/70 backdrop-blur-xl border border-white/60 rounded-3xl shadow-xl p-8 lg:p-12">
              <div class="flex items-center mb-8">
                <div class="flex-shrink-0 w-12 h-12 bg-gradient-to-r from-emerald-500 to-teal-500 rounded-xl flex items-center justify-center shadow-lg">
                  <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"></path>
                  </svg>
                </div>
                <div class="ml-6">
                  <h2 class="text-2xl lg:text-3xl font-bold text-slate-900">Research Summary</h2>
                  <p class="text-slate-600 mt-1">AI-generated insights from your search results</p>
                </div>
              </div>
              
              <div class="prose prose-lg max-w-none">
                <p class="text-slate-700 leading-relaxed whitespace-pre-line text-base lg:text-lg">{{ processedSummaryAndReferences.summaryText }}</p>
              </div>
              
              <div v-if="processedSummaryAndReferences.references.length > 0" class="mt-10 pt-8 border-t border-slate-200/60">
                <h3 class="text-xl font-bold text-slate-800 mb-6 flex items-center">
                  <svg class="w-5 h-5 mr-3 text-slate-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.746 0 3.332.477 4.5 1.253v13C19.832 18.477 18.246 18 16.5 18c-1.746 0-3.332.477-4.5 1.253"></path>
                  </svg>
                  References
                </h3>
                <div class="grid gap-3">
                  <div v-for="ref in processedSummaryAndReferences.references" :key="ref.index" 
                       class="flex items-start p-4 bg-slate-50/50 rounded-xl hover:bg-slate-100/50 transition-colors duration-200 group/ref">
                    <span class="flex-shrink-0 w-8 h-8 bg-gradient-to-r from-blue-500 to-indigo-500 text-white text-sm font-bold rounded-lg flex items-center justify-center mr-4">
                      {{ ref.index }}
                    </span>
                    <a href="#" @click.prevent="handleReferenceClick(ref.db_id)" 
                       class="text-slate-700 hover:text-blue-600 transition-colors duration-200 group-hover/ref:text-blue-600 font-medium flex-1"
                       :title="`Go to paper: ${ref.title}`">
                      {{ ref.title }}
                      <span class="text-xs text-slate-500 ml-2 font-normal">(ID: {{ ref.source_id || ref.db_id }})</span>
                    </a>
                    <svg class="w-4 h-4 text-slate-400 group-hover/ref:text-blue-500 transition-colors duration-200 opacity-0 group-hover/ref:opacity-100" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7l5 5m0 0l-5 5m5-5H6"></path>
                    </svg>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
        
        <!-- Papers List Section -->
        <div class="group">
          <div class="relative">
            <div class="absolute inset-0 bg-gradient-to-r from-blue-500/10 to-purple-500/10 rounded-3xl blur-xl opacity-70 group-hover:opacity-100 transition-opacity duration-300"></div>
            <div class="relative bg-white/70 backdrop-blur-xl border border-white/60 rounded-3xl shadow-xl overflow-hidden">
              <!-- Header -->
              <div class="bg-gradient-to-r from-slate-50/80 to-slate-100/80 backdrop-blur-sm p-8 border-b border-slate-200/60">
                <div class="flex flex-col lg:flex-row justify-between lg:items-center gap-6">
                  <div class="flex items-center">
                    <div class="flex-shrink-0 w-12 h-12 bg-gradient-to-r from-blue-500 to-purple-500 rounded-xl flex items-center justify-center shadow-lg">
                      <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
                      </svg>
                    </div>
                    <div class="ml-6">
                      <h2 class="text-2xl lg:text-3xl font-bold text-slate-900">
                        Research Papers
                      </h2>
                      <p class="text-slate-600 mt-1">{{ processedPapers.length }} papers found</p>
                    </div>
                  </div>
                  
                  <!-- Chat Button -->
                  <div v-if="selectedPapersForChat.size > 0" class="flex-shrink-0">
                    <button @click="startChatting" 
                            class="inline-flex items-center px-8 py-4 bg-gradient-to-r from-emerald-500 to-teal-500 text-white font-semibold rounded-xl shadow-lg hover:from-emerald-600 hover:to-teal-600 focus:outline-none focus:ring-4 focus:ring-emerald-500/50 transition-all duration-200 transform hover:scale-105 active:scale-95">
                      <svg class="w-5 h-5 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"></path>
                      </svg>
                      Chat with {{ selectedPapersForChat.size }} Selected Paper{{ selectedPapersForChat.size > 1 ? 's' : '' }}
                      <div class="ml-2 w-6 h-6 bg-white/20 rounded-full flex items-center justify-center text-sm font-bold">
                        {{ selectedPapersForChat.size }}
                      </div>
                    </button>
                  </div>
                </div>
              </div>
              
              <!-- Papers List -->
              <div class="p-8">
                <PaperList :papers="processedPapers" @update-paper-selection="updateSelectedPapers" />
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Empty State -->
    <div v-else-if="!isLoadingSearch && !searchQuerySubmitted" class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-20">
      <div class="text-center">
        <div class="relative">
          <div class="absolute inset-0 bg-gradient-to-r from-slate-200/50 to-slate-300/50 rounded-3xl blur-xl"></div>
          <div class="relative bg-white/60 backdrop-blur-xl border border-white/60 rounded-3xl shadow-xl p-12 lg:p-20">
            <div class="w-24 h-24 bg-gradient-to-r from-slate-400 to-slate-500 rounded-full flex items-center justify-center mx-auto mb-8 shadow-lg">
              <svg class="w-12 h-12 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path>
              </svg>
            </div>
            <h3 class="text-2xl font-bold text-slate-800 mb-4">Ready to Explore</h3>
            <p class="text-lg text-slate-600 leading-relaxed">Enter your research query above and click "Search Papers" to discover relevant academic papers and insights.</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Chat Modal -->
    <div v-if="isChatting" class="fixed inset-0 bg-slate-900/50 backdrop-blur-sm flex items-center justify-center z-50 p-4">
      <div class="bg-white/95 backdrop-blur-xl w-full max-w-5xl h-[calc(100vh-4rem)] flex flex-col overflow-hidden rounded-3xl shadow-2xl border border-white/60">
        <ChatInterface
          :selected-paper-ids="Array.from(selectedPapersForChat)"
          :papers-in-context="processedPapers" 
          :current-chat-session-id="currentChatSessionIdForView" 
          @session-updated="handleSessionUpdated"
          @chat-closed="isChatting = false" 
          class="flex-grow min-h-0"
        />
        <div class="flex-shrink-0 p-6 bg-slate-50/80 backdrop-blur-sm border-t border-slate-200/60">
          <button @click="closeChatAndClearSession" 
                  class="w-full sm:w-auto block mx-auto px-8 py-3 bg-gradient-to-r from-red-500 to-red-600 text-white font-semibold rounded-xl shadow-lg hover:from-red-600 hover:to-red-700 focus:outline-none focus:ring-4 focus:ring-red-500/50 transition-all duration-200 transform hover:scale-105 active:scale-95">
            <div class="flex items-center justify-center">
              <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
              </svg>
              Close Chat
            </div>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onBeforeUnmount, watch, computed } from 'vue';
import * as paperService from '@/services/paperService';
import type { Paper, PaperSearchResponse, PaperStatusResponse, ChatMessage } from '@/types';
import PaperList from '@/components/paper/PaperList.vue';
import ChatInterface from '@/components/chat/ChatInterface.vue';

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

const currentChatSessionIdForView = ref<number | null>(null);

const clearAllPollingIntervals = () => {
  pollingIntervals.value.forEach(intervalId => clearInterval(intervalId));
  pollingIntervals.value.clear();
};

onBeforeUnmount(() => {
  clearAllPollingIntervals();
});

const processedSummaryAndReferences = computed(() => {
  if (!searchResults.value?.consolidated_summary) {
    return { summaryText: '', references: [] };
  }

  const summary = searchResults.value.consolidated_summary;
  const referencesMap = new Map<string, { index: number; title: string; db_id: number; source_id: string }>();
  const referencesList: Array<{ index: number; title: string; db_id: number; source_id: string }> = [];
  let referenceIndex = 0;

  // Regex to find citations like [xxxx.yyyyy], [xxxx.yyyyyvN], or [DB_ID_as_string]
  const citationRegex = /\[([^\]]+?)\]/g;

  const transformedSummaryText = summary.replace(citationRegex, (match, citedIdentifier) => {
    const trimmedIdentifier = citedIdentifier.trim();
    
    if (referencesMap.has(trimmedIdentifier)) {
      return `[${referencesMap.get(trimmedIdentifier)!.index}]`;
    }

    // Attempt to find the paper in processedPapers by source_id (e.g., arXiv ID) or db_id
    const paper = processedPapers.value.find(p => 
        p.paper_id === trimmedIdentifier || 
        p.db_id.toString() === trimmedIdentifier
    );

    if (paper) {
      referenceIndex++;
      const refData = {
        index: referenceIndex,
        title: paper.title,
        db_id: paper.db_id,
        source_id: paper.paper_id || paper.db_id.toString(), // Store the identifier that was matched or db_id as fallback
      };
      referencesMap.set(trimmedIdentifier, refData); // Use the original identifier as key
      referencesList.push(refData);
      return `[${referenceIndex}]`;
    } else {
      // If paper not found in current results, keep original citation
      // console.warn(`Cited paper with identifier "${trimmedIdentifier}" not found in processedPapers.`);
      return match; 
    }
  });

  return {
    summaryText: transformedSummaryText,
    references: referencesList.sort((a, b) => a.index - b.index), // Ensure sorted by appearance
  };
});

const handleReferenceClick = (paperDbId: number) => {
  const paperElement = document.getElementById(`paper-item-${paperDbId}`);
  if (paperElement) {
    paperElement.scrollIntoView({ behavior: 'smooth', block: 'center' });
    // Optional: Add a temporary highlight effect
    paperElement.classList.add('highlight-flash');
    setTimeout(() => {
      paperElement.classList.remove('highlight-flash');
    }, 1500);
  } else {
    console.warn(`Paper element with ID paper-item-${paperDbId} not found for scrolling.`);
  }
};


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

        if (statusResponse.processing_status_notes && statusResponse.processing_status_notes !== 'arXiv' && statusResponse.processing_status_notes.match(/Failed|Error/i)) {
          paperToUpdate.processing_status_message = statusResponse.processing_status_notes;
        } else if (paperToUpdate.retryInitiated && !paperToUpdate.processing_status_message?.startsWith('Retry failed:')) {
           paperToUpdate.processing_status_message = 'Processing... (after retry attempt)';
        } else if (!paperToUpdate.retryInitiated) { 
          paperToUpdate.processing_status_message = 'Processing...';
        }

        if (paperToUpdate.pollingAttempts >= MAX_POLLING_ATTEMPTS_BEFORE_RETRY && 
            !paperToUpdate.retryInitiated && 
            paperToUpdate.is_polling_status) {
          
          paperToUpdate.retryInitiated = true; 
          paperToUpdate.processing_status_message = 'Retrying processing...'; 
          
          console.log(`Attempting to manually re-process paper ${paperDbId} after ${paperToUpdate.pollingAttempts} attempts.`);
          try {
            await paperService.retryProcessPaper(paperDbId);
            console.log(`Manual processing re-initiated for paper ${paperDbId}.`);
            paperToUpdate.pollingAttempts = 0;
          } catch (retryError: any) {
            console.error(`Failed to trigger retry for paper ${paperDbId}:`, retryError);
            paperToUpdate.processing_status_message = `Retry failed: ${retryError.response?.data?.msg || retryError.message || 'Unknown error'}`;
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
  
  // When a new search happens, we should probably reset any ongoing chat session ID
  currentChatSessionIdForView.value = null; 
  isChatting.value = false; // Close chat window on new search

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
    // When starting a new chat, if the selected papers change, we might want to reset the session ID.
    // For now, we'll let ChatInterface handle its session or start a new one.
    // If we wanted to be more explicit, we could reset currentChatSessionIdForView.value = null here
    // if the set of selected papers has changed since the last chat.
    console.log('Start chatting with papers:', Array.from(selectedPapersForChat.value));
    isChatting.value = true;
  } else {
    alert('Please select at least one paper that is ready for chat.');
  }
};

const handleSessionUpdated = (newSessionId: number) => {
  currentChatSessionIdForView.value = newSessionId;
  console.log('Chat session updated in ResearchView, new ID:', newSessionId);
};

const closeChatAndClearSession = () => {
  isChatting.value = false;
  // Optionally, you might want to clear the currentChatSessionIdForView if closing means "ending" the session.
  // currentChatSessionIdForView.value = null; 
  // This depends on whether closing the modal should forget the session or allow resuming later.
  // For now, just closing the modal.
};


watch(selectedPapersForChat, (newSelection) => {
  // console.log('Selected papers changed:', newSelection);
}, { deep: true });

</script>

<style scoped>
.whitespace-pre-line {
  white-space: pre-line;
}

.highlight-flash {
  transition: background-color 0.8s ease-in-out;
  background-color: #dbeafe !important; /* Tailwind's blue-100 */
  border-radius: 1rem;
  box-shadow: 0 0 0 4px rgba(59, 130, 246, 0.3);
}

.prose {
  max-width: none;
}

.prose p {
  margin-bottom: 1.25em;
  line-height: 1.75;
}

/* Custom scrollbar for better aesthetics */
::-webkit-scrollbar {
  width: 8px;
  height: 8px;
}

::-webkit-scrollbar-track {
  background: #f1f5f9;
  border-radius: 4px;
}

::-webkit-scrollbar-thumb {
  background: linear-gradient(to bottom, #64748b, #475569);
  border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
  background: linear-gradient(to bottom, #475569, #334155);
}

/* Enhance hover effects */
.group:hover .highlight-flash {
  background-color: #eff6ff !important;
}

/* Smooth transitions for all interactive elements */
* {
  transition-property: color, background-color, border-color, text-decoration-color, fill, stroke, opacity, box-shadow, transform, filter, backdrop-filter;
  transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);
  transition-duration: 200ms;
}

/* Enhanced focus states */
input:focus, button:focus {
  outline: none;
  box-shadow: 0 0 0 4px rgba(59, 130, 246, 0.1);
}

/* Loading animation refinements */
@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.animate-spin {
  animation: spin 1s linear infinite;
}

/* Backdrop blur fallback */
@supports not (backdrop-filter: blur(12px)) {
  .backdrop-blur-xl {
    background-color: rgba(255, 255, 255, 0.9);
  }
  
  .backdrop-blur-sm {
    background-color: rgba(255, 255, 255, 0.8);
  }
}

/* Mobile optimizations */
@media (max-width: 640px) {
  .text-4xl {
    font-size: 2.5rem;
  }
  
  .text-6xl {
    font-size: 3rem;
  }
  
  .p-8 {
    padding: 1.5rem;
  }
  
  .p-12 {
    padding: 2rem;
  }
}
</style>