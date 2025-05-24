<template>
  <div class="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-50">
    <div class="container mx-auto px-4 sm:px-6 lg:px-8 py-8 sm:py-12">
      <!-- Header Section -->
      <div class="text-center mb-12">
        <div class="inline-flex items-center justify-center w-16 h-16 bg-gradient-to-r from-indigo-500 to-purple-600 rounded-2xl shadow-lg mb-6">
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="w-8 h-8 text-white">
            <path stroke-linecap="round" stroke-linejoin="round" d="M8.625 12a.375.375 0 11-.75 0 .375.375 0 01.75 0zm0 0H8.25m4.125 0a.375.375 0 11-.75 0 .375.375 0 01.75 0zm0 0H12m4.125 0a.375.375 0 11-.75 0 .375.375 0 01.75 0zm0 0h-.375M21 12c0 4.556-4.03 8.25-9 8.25a9.764 9.764 0 01-2.555-.337A5.972 5.972 0 015.41 20.97a5.969 5.969 0 01-.474-.065 4.48 4.48 0 00.978-2.025c.09-.457-.133-.901-.467-1.226C3.93 16.178 3 14.189 3 12c0-4.556 4.03-8.25 9-8.25s9 3.694 9 8.25z" />
          </svg>
        </div>
        <h1 class="text-4xl sm:text-5xl font-bold bg-gradient-to-r from-slate-800 via-indigo-600 to-purple-600 bg-clip-text text-transparent mb-4">
          <span class="text-indigo-600">Chat History</span>
        </h1>
        <p class="text-lg text-slate-600 max-w-2xl mx-auto">
          Review and manage your research conversations with Lexify AI
        </p>
      </div>

      <!-- Loading State -->
      <div v-if="isLoading" class="flex flex-col items-center justify-center py-20">
        <div class="relative">
          <div class="w-16 h-16 border-4 border-indigo-200 rounded-full animate-spin"></div>
          <div class="absolute top-0 left-0 w-16 h-16 border-4 border-transparent border-t-indigo-600 rounded-full animate-spin"></div>
        </div>
        <p class="mt-6 text-lg text-slate-600 font-medium">Loading your conversations...</p>
        <p class="text-sm text-slate-500 mt-2">This might take a moment</p>
      </div>

      <!-- Error State -->
      <div v-if="error" class="max-w-2xl mx-auto mb-8">
        <div class="bg-gradient-to-r from-red-50 to-pink-50 border border-red-200 rounded-2xl p-6 shadow-sm">
          <div class="flex items-start">
            <div class="flex-shrink-0">
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="w-6 h-6 text-red-500">
                <path stroke-linecap="round" stroke-linejoin="round" d="M12 9v3.75m9-.75a9 9 0 11-18 0 9 9 0 0118 0zm-9 3.75h.008v.008H12v-.008z" />
              </svg>
            </div>
            <div class="ml-4">
              <h3 class="text-lg font-semibold text-red-800 mb-1">Unable to Load Chat History</h3>
              <p class="text-red-700">{{ error }}</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Empty State -->
      <div v-if="!isLoading && !error && sessions.length === 0" class="max-w-2xl mx-auto">
        <div class="bg-white/70 backdrop-blur-sm border border-slate-200 rounded-3xl p-12 text-center shadow-xl">
          <div class="w-20 h-20 bg-gradient-to-r from-slate-100 to-slate-200 rounded-full flex items-center justify-center mx-auto mb-6">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-10 h-10 text-slate-400">
              <path stroke-linecap="round" stroke-linejoin="round" d="M20.25 8.511c.884.284 1.5 1.128 1.5 2.097v4.286c0 1.136-.847 2.1-1.96 2.193-.34.027-.68.052-1.02.072v3.091l-3-3c-1.354 0-2.694-.055-4.02-.163a2.115 2.115 0 01-.825-.242m9.345-8.334a2.126 2.126 0 00-.476-.095 48.64 48.64 0 00-8.048 0c-1.131.094-1.976 1.057-1.976 2.192v4.286c0 .837.46 1.58 1.155 1.951m9.345-8.334V6.637c0-1.621-1.152-3.026-2.76-3.235A48.455 48.455 0 0011.25 3c-2.115 0-4.198.137-6.24.402-1.608.209-2.76 1.614-2.76 3.235v6.226c0 1.621 1.152 3.026 2.76 3.235.577.075 1.157.14 1.74.194V21l4.155-4.155" />
            </svg>
          </div>
          <h2 class="text-2xl font-bold text-slate-800 mb-4">No Conversations Yet</h2>
          <p class="text-slate-600 mb-8 text-lg">Your research conversations will appear here once you start chatting with Lexify AI.</p>
          <button @click="$router.push({ name: 'Research' })" 
                  class="inline-flex items-center px-8 py-4 bg-gradient-to-r from-indigo-600 to-purple-600 text-white font-semibold rounded-2xl shadow-lg hover:from-indigo-700 hover:to-purple-700 transform hover:scale-105 transition-all duration-200">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="w-5 h-5 mr-2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M12 4.5v15m7.5-7.5h-15" />
            </svg>
            Start New Research
          </button>
        </div>
      </div>

      <!-- Chat Sessions Grid -->
      <div v-if="!isLoading && sessions.length > 0" class="grid gap-6 md:gap-8">
        <div v-for="session in sessions" :key="session.id" 
             class="group bg-white/70 backdrop-blur-sm border border-slate-200 rounded-3xl overflow-hidden shadow-lg hover:shadow-2xl hover:scale-[1.02] transition-all duration-300 cursor-pointer"
             @click="selectSession(session.id)">
          
          <!-- Session Header -->
          <div class="p-6 sm:p-8 border-b border-slate-100">
            <div class="flex flex-col sm:flex-row sm:items-start sm:justify-between gap-4">
              <div class="flex-1 min-w-0">
                <h3 class="text-xl sm:text-2xl font-bold text-slate-800 mb-2 truncate group-hover:text-indigo-600 transition-colors duration-200" 
                    :title="session.session_name || (session.paper_titles_in_session && session.paper_titles_in_session.length > 0 ? `Session with: ${session.paper_titles_in_session.join(', ')}` : `Session ${session.id}`)">
                  {{ session.session_name || (session.paper_titles_in_session && session.paper_titles_in_session.length > 0 ? `Session with: ${session.paper_titles_in_session.join(', ')}` : `Session ${session.id}`) }}
                </h3>
                <div class="flex items-center text-sm text-slate-500 mb-3">
                  <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-4 h-4 mr-2">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M15.75 5.25a3 3 0 013 3m3 0a6 6 0 01-7.029 5.912c-.563-.097-1.159.026-1.563.43L10.5 17.25H8.25v2.25H6v2.25H2.25v-2.818c0-.597.237-1.17.659-1.591l6.499-6.499c.404-.404.527-1 .43-1.563A6 6 0 1121.75 8.25z" />
                  </svg>
                  Session ID: {{ session.id }}
                </div>
              </div>
              <div class="flex-shrink-0">
                <span class="inline-flex items-center px-4 py-2 bg-gradient-to-r from-slate-100 to-slate-200 text-slate-700 text-sm font-medium rounded-full">
                  <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-4 h-4 mr-2">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M12 6v6h4.5m4.5 0a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                  {{ formatDate(session.updated_at) }}
                </span>
              </div>
            </div>
          </div>

          <!-- Session Content -->
          <div class="p-6 sm:p-8">
            <div class="mb-4">
              <div class="flex items-center justify-between mb-3">
                <h4 class="text-sm font-semibold text-slate-700 uppercase tracking-wider">Research Papers</h4>
                <span class="inline-flex items-center justify-center min-w-[24px] h-6 bg-indigo-100 text-indigo-700 text-xs font-bold rounded-full px-2">
                  {{ session.paper_titles_in_session?.length || 0 }}
                </span>
              </div>
              
              <div v-if="session.paper_titles_in_session && session.paper_titles_in_session.length > 0" 
                   class="space-y-2">
                <div v-for="(title, index) in session.paper_titles_in_session.slice(0, 3)" :key="index"
                     class="flex items-start">
                  <div class="w-2 h-2 bg-indigo-400 rounded-full mt-2 mr-3 flex-shrink-0"></div>
                  <p class="text-sm text-slate-600 font-medium leading-relaxed" :title="title">
                    {{ title.length > 80 ? title.substring(0, 80) + '...' : title }}
                  </p>
                </div>
                <div v-if="session.paper_titles_in_session.length > 3" 
                     class="flex items-center mt-2">
                  <div class="w-2 h-2 bg-slate-300 rounded-full mr-3"></div>
                  <p class="text-sm text-slate-500 italic">
                    +{{ session.paper_titles_in_session.length - 3 }} more papers
                  </p>
                </div>
              </div>
              
              <div v-else-if="session.paper_ids_in_session && session.paper_ids_in_session.length > 0" 
                   class="flex items-center">
                <div class="w-2 h-2 bg-amber-400 rounded-full mr-3"></div>
                <p class="text-sm text-slate-600">
                  Paper IDs: {{ session.paper_ids_in_session.join(', ') }}
                  <span class="text-slate-500 italic ml-2">(Titles not available)</span>
                </p>
              </div>
              
              <div v-else class="flex items-center">
                <div class="w-2 h-2 bg-slate-300 rounded-full mr-3"></div>
                <p class="text-sm text-slate-500 italic">No specific papers linked to this session</p>
              </div>
            </div>

            <!-- Action Hint -->
            <div class="flex items-center justify-between pt-4 border-t border-slate-100">
              <p class="text-sm text-slate-500 italic">Click to view conversation details</p>
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="w-5 h-5 text-slate-400 group-hover:text-indigo-500 transition-colors duration-200">
                <path stroke-linecap="round" stroke-linejoin="round" d="M13.5 4.5L21 12m0 0l-7.5 7.5M21 12H3" />
              </svg>
            </div>
          </div>
        </div>
      </div>

      <!-- Enhanced Modal for Chat Messages -->
      <div v-if="selectedSessionData" 
           class="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-50 p-4"
           @click.self="closeMessagesModal">
        <div class="bg-white w-full max-w-5xl h-[90vh] flex flex-col rounded-3xl shadow-2xl overflow-hidden">
          
          <!-- Modal Header -->
          <header class="relative p-6 border-b border-slate-200 bg-gradient-to-r from-indigo-50 to-purple-50">
            <div class="flex items-start justify-between">
              <div class="flex-1 min-w-0 pr-4">
                <h3 class="text-xl sm:text-2xl font-bold text-slate-800 mb-2 truncate">
                  {{ selectedSessionData.session_name || (selectedSessionData.associated_paper_titles && selectedSessionData.associated_paper_titles.length > 0 ? `Chat with: ${selectedSessionData.associated_paper_titles.join(', ')}` : `Chat Details (Session: ${selectedSessionData.session_id})`) }}
                </h3>
                <p class="text-sm text-slate-600">Session ID: {{ selectedSessionData.session_id }}</p>
              </div>
              <button @click="closeMessagesModal" 
                      class="flex-shrink-0 p-2 text-slate-500 hover:text-slate-700 hover:bg-white rounded-xl transition-all duration-200">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="w-6 h-6">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>
          </header>

          <!-- Papers Info -->
          <div v-if="selectedSessionData && selectedSessionData.associated_paper_titles && selectedSessionData.associated_paper_titles.length > 0" 
               class="px-6 py-4 border-b border-slate-200 bg-slate-50">
            <div class="flex items-center mb-2">
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-5 h-5 text-indigo-600 mr-2">
                <path stroke-linecap="round" stroke-linejoin="round" d="M19.5 14.25v-2.625a3.375 3.375 0 00-3.375-3.375h-1.5A1.125 1.125 0 0113.5 7.125v-1.5a3.375 3.375 0 00-3.375-3.375H8.25m0 12.75h7.5m-7.5 3H12M10.5 2.25H5.625c-.621 0-1.125.504-1.125 1.125v17.25c0 .621.504 1.125 1.125 1.125h12.75c.621 0-1.125.504-1.125 1.125V11.25a9 9 0 00-9-9z" />
              </svg>
              <span class="text-sm font-semibold text-slate-700">Research Papers in this conversation:</span>
            </div>
            <p class="text-sm text-slate-600 leading-relaxed">{{ selectedSessionData.associated_paper_titles.join(', ') }}</p>
          </div>

          <!-- Messages Loading -->
          <div v-if="isLoadingMessages" class="flex-grow flex items-center justify-center">
            <div class="text-center">
              <div class="relative mb-4">
                <div class="w-12 h-12 border-4 border-indigo-200 rounded-full animate-spin"></div>
                <div class="absolute top-0 left-0 w-12 h-12 border-4 border-transparent border-t-indigo-600 rounded-full animate-spin"></div>
              </div>
              <p class="text-slate-600 font-medium">Loading conversation...</p>
            </div>
          </div>

          <!-- Messages Error -->
          <div v-if="messagesError" class="flex-grow flex items-center justify-center p-6">
            <div class="text-center max-w-md">
              <div class="w-16 h-16 bg-red-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="w-8 h-8 text-red-500">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M12 9v3.75m9-.75a9 9 0 11-18 0 9 9 0 0118 0zm-9 3.75h.008v.008H12v-.008z" />
                </svg>
              </div>
              <h3 class="text-lg font-semibold text-slate-800 mb-2">Failed to Load Messages</h3>
              <p class="text-red-600">{{ messagesError }}</p>
            </div>
          </div>

          <!-- Messages Container -->
          <div v-if="!isLoadingMessages && selectedSessionData && selectedSessionData.messages.length > 0" 
               ref="messageContainerModal" 
               class="flex-grow p-6 space-y-6 overflow-y-auto bg-gradient-to-b from-slate-50 to-white">
            
            <div v-for="(message, index) in selectedSessionData.messages" :key="message.id || index" 
                 :class="messageBubbleClass(message.role)">
              <div :class="messageContentClass(message.role)">
                <!-- Message Content -->
                <div v-if="message.role === 'assistant'" 
                     class="prose prose-sm max-w-none prose-indigo" 
                     v-html="renderMarkdown(message.content)"></div>
                <p v-else class="whitespace-pre-line leading-relaxed">{{ message.content }}</p>
                
                <!-- Sources -->
                <div v-if="message.role === 'assistant' && message.sources && Object.keys(message.sources).length > 0" 
                     class="mt-4 pt-4 border-t border-slate-200">
                  <div class="flex items-center mb-3">
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-4 h-4 text-indigo-600 mr-2">
                      <path stroke-linecap="round" stroke-linejoin="round" d="M13.19 8.688a4.5 4.5 0 011.242 7.244l-4.5 4.5a4.5 4.5 0 01-6.364-6.364l1.757-1.757m13.35-.622l1.757-1.757a4.5 4.5 0 00-6.364-6.364l-4.5 4.5a4.5 4.5 0 001.242 7.244" />
                    </svg>
                    <span class="text-sm font-semibold text-slate-700">Sources Referenced:</span>
                  </div>
                  <div class="grid gap-2">
                    <div v-for="(source, key) in message.sources" :key="key" 
                         class="flex items-start p-3 bg-slate-50 rounded-xl hover:bg-slate-100 transition-colors duration-200 cursor-pointer"
                         :title="`Source: ${source.title || key}\nContext: ${source.text}`">
                      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16" fill="currentColor" class="w-4 h-4 text-indigo-500 mr-3 mt-0.5 flex-shrink-0">
                        <path d="M3.5 2A1.5 1.5 0 0 0 2 3.5v9A1.5 1.5 0 0 0 3.5 14h9a1.5 1.5 0 0 0 1.5-1.5V6.528a1.5 1.5 0 0 0-.44-1.06L9.53 2.439A1.5 1.5 0 0 0 8.472 2H3.5ZM8 6V3.5L12.5 8H9a1 1 0 0 1-1-1Z" />
                      </svg>
                      <span class="text-sm text-slate-700 font-medium leading-relaxed">{{ source.title || key }}</span>
                    </div>
                  </div>
                </div>
                
                <!-- Timestamp -->
                <div v-if="message.timestamp" class="flex justify-end mt-3">
                  <span class="text-xs text-slate-500 bg-slate-100 px-3 py-1 rounded-full">
                    {{ formatTimestamp(message.timestamp) }}
                  </span>
                </div>
              </div>
            </div>
          </div>

          <!-- Empty Messages -->
          <div v-if="!isLoadingMessages && selectedSessionData && selectedSessionData.messages.length === 0 && !messagesError" 
               class="flex-grow flex items-center justify-center">
            <div class="text-center max-w-md">
              <div class="w-16 h-16 bg-slate-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-8 h-8 text-slate-400">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M20.25 8.511c.884.284 1.5 1.128 1.5 2.097v4.286c0 1.136-.847 2.1-1.96 2.193-.34.027-.68.052-1.02.072v3.091l-3-3c-1.354 0-2.694-.055-4.02-.163a2.115 2.115 0 01-.825-.242m9.345-8.334a2.126 2.126 0 00-.476-.095 48.64 48.64 0 00-8.048 0c-1.131.094-1.976 1.057-1.976 2.192v4.286c0 .837.46 1.58 1.155 1.951m9.345-8.334V6.637c0-1.621-1.152-3.026-2.76-3.235A48.455 48.455 0 0011.25 3c-2.115 0-4.198.137-6.24.402-1.608.209-2.76 1.614-2.76 3.235v6.226c0 1.621 1.152 3.026 2.76 3.235.577.075 1.157.14 1.74.194V21l4.155-4.155" />
                </svg>
              </div>
              <h3 class="text-lg font-semibold text-slate-800 mb-2">No Messages Found</h3>
              <p class="text-slate-600">This conversation doesn't have any messages yet.</p>
            </div>
          </div>

          <!-- Modal Footer -->
          <footer class="p-6 border-t border-slate-200 bg-gradient-to-r from-slate-50 to-slate-100">
            <div class="flex justify-center">
              <button @click="resumeChat" 
                      :disabled="!selectedSessionData"
                      class="inline-flex items-center px-8 py-4 bg-gradient-to-r from-green-600 to-emerald-600 text-white font-semibold rounded-2xl shadow-lg hover:from-green-700 hover:to-emerald-700 focus:ring-4 focus:ring-green-300 transform hover:scale-105 transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="w-5 h-5 mr-2">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M5.25 5.653c0-.856.917-1.398 1.667-.986l11.54 6.348a1.125 1.125 0 010 1.971l-11.54 6.347a1.125 1.125 0 01-1.667-.985V5.653z" />
                </svg>
                Resume Conversation
              </button>
            </div>
          </footer>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, nextTick } from 'vue';
import { useRouter } from 'vue-router';
import * as ragService from '@/services/ragService';
// Ensure your types match the API responses
import type { ChatSessionInfo, ChatMessage, FullChatSession, Source } from '@/types'; 
import { marked } from 'marked';
import DOMPurify from 'dompurify';

const router = useRouter();
const sessions = ref<ChatSessionInfo[]>([]);
const isLoading = ref(true);
const error = ref<string | null>(null);

// Store the entire FullChatSession object when a session is selected
const selectedSessionData = ref<FullChatSession | null>(null); 
const isLoadingMessages = ref(false);
const messagesError = ref<string | null>(null);
// showMessagesModal is implicitly handled by selectedSessionData being non-null
const messageContainerModal = ref<HTMLElement | null>(null);


const fetchSessions = async () => {
  isLoading.value = true;
  error.value = null;
  try {
    // Assuming listChatSessions returns ChatSessionInfo[]
    sessions.value = await ragService.listChatSessions();
  } catch (err: any) {
    console.error('Failed to fetch chat sessions:', err);
    error.value = err.response?.data?.msg || err.message || 'Could not load chat history.';
  } finally {
    isLoading.value = false;
  }
};

const selectSession = async (sessionId: number) => {
  selectedSessionData.value = null; // Clear previous selection
  isLoadingMessages.value = true;
  messagesError.value = null;

  try {
    // getChatSessionMessages returns FullChatSession
    const fullSession = await ragService.getChatSessionMessages(sessionId);
    selectedSessionData.value = fullSession;
    nextTick(scrollToBottomModal);
  } catch (err: any) {
    console.error(`Failed to fetch messages for session ${sessionId}:`, err);
    messagesError.value = err.response?.data?.msg || err.message || 'Could not load messages for this session.';
  } finally {
    isLoadingMessages.value = false;
  }
};

const closeMessagesModal = () => {
  selectedSessionData.value = null;
};

const resumeChat = () => {
  if (!selectedSessionData.value) return;
  
  const sessionToResume = sessions.value.find(s => s.id === selectedSessionData.value!.session_id);
  let paperIdsToPass: number[] = [];

  if (sessionToResume) {
    paperIdsToPass = sessionToResume.paper_ids_in_session;
  } else if (selectedSessionData.value.messages.length > 0) {
    // Fallback: try to get paper IDs from the detailed session data if list item not found
    // This depends on whether your FullChatSession includes paper_ids_in_session
    // For now, we'll rely on the original session list item.
    // If your FullChatSession from getChatSessionMessages also includes the raw paper_db_ids, use that.
    // For now, we assume the original `sessions` list is the source for `paper_ids_in_session`.
    console.warn("Could not find original session item to get paper_ids_in_session for resume. Resuming without pre-selecting papers by ID.");
  }

  router.push({ 
    name: 'Research', 
    query: { 
      resume_session_id: selectedSessionData.value.session_id,
      // Pass paper IDs if available and needed by ResearchView to pre-select
      paper_ids: paperIdsToPass.length > 0 ? paperIdsToPass.join(',') : undefined
    } 
  });
  closeMessagesModal();
};

const formatDate = (dateString: string) => {
  if (!dateString) return 'N/A';
  return new Date(dateString).toLocaleString([], { dateStyle: 'medium', timeStyle: 'short' });
};

const renderMarkdown = (content: string) => {
  if (!content) return '';
  let linkedContent = content.replace(/\[(.*?)\]/g, (match, innerContent) => {
    const ids = innerContent.split(',').map(id => id.trim()).filter(id => id);
    if (ids.length === 0) return match;
    const links = ids.map(paperId => {
      const cleanPaperId = paperId.replace(/[^A-Za-z0-9.-v]/g, '');
      if (!cleanPaperId) return paperId;
      // In a read-only history view, alerts are fine for citations.
      return `<a href="#" data-paper-id="${cleanPaperId}" class="text-indigo-600 hover:underline font-medium" onclick="event.preventDefault(); alert('Cited Paper ID: ${cleanPaperId}');">${paperId}</a>`;
    });
    return `[${links.join(', ')}]`;
  });
  const rawHtml = marked.parse(linkedContent) as string;
  // Ensure ADD_ATTR allows 'onclick' if you keep the inline alert, or handle clicks via event delegation.
  return DOMPurify.sanitize(rawHtml, { ADD_ATTR: ['data-paper-id', 'onclick'], ADD_TAGS: ['a'], ALLOWED_URI_REGEXP: /^(?:(?:(?:f|ht)tps?|mailto|tel|callto|cid|xmpp):|#)/i });
};

const messageBubbleClass = (role: 'user' | 'assistant') => {
  return role === 'user' ? 'flex justify-end' : 'flex justify-start';
};

const messageContentClass = (role: 'user' | 'assistant') => {
  let baseClass = 'p-4 sm:p-6 rounded-2xl max-w-2xl shadow-sm';
  if (role === 'user') {
    return `${baseClass} bg-gradient-to-r from-indigo-600 to-purple-600 text-white`;
  }
  return `${baseClass} bg-white border border-slate-200 text-slate-800`;
};

const formatTimestamp = (isoString?: string) => {
  if (!isoString) return '';
  return new Date(isoString).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
};

const scrollToBottomModal = () => {
  if (messageContainerModal.value) {
    messageContainerModal.value.scrollTop = messageContainerModal.value.scrollHeight;
  }
};

onMounted(() => {
  fetchSessions();
});
</script>

<style scoped>
/* Enhanced prose styling for message content */
.prose-indigo {
  --tw-prose-body: theme('colors.slate.700');
  --tw-prose-headings: theme('colors.slate.900');
  --tw-prose-lead: theme('colors.slate.600');
  --tw-prose-links: theme('colors.indigo.600');
  --tw-prose-bold: theme('colors.slate.900');
  --tw-prose-counters: theme('colors.slate.500');
  --tw-prose-bullets: theme('colors.slate.300');
  --tw-prose-hr: theme('colors.slate.200');
  --tw-prose-quotes: theme('colors.slate.900');
  --tw-prose-quote-borders: theme('colors.slate.200');
  --tw-prose-captions: theme('colors.slate.500');
}

.prose :where(ul):not(:where([class~="not-prose"] *)) {
  list-style-type: disc;
  padding-left: 1.5em;
  margin-top: 1em;
  margin-bottom: 1em;
}

.prose :where(ol):not(:where([class~="not-prose"] *)) {
  list-style-type: decimal;
  padding-left: 1.5em;
  margin-top: 1em;
  margin-bottom: 1em;
}

.prose :where(li):not(:where([class~="not-prose"] *)) {
  margin-top: 0.5em;
  margin-bottom: 0.5em;
}

.prose :where(strong):not(:where([class~="not-prose"] *)) {
  font-weight: 600;
  color: var(--tw-prose-bold);
}

.prose :where(a):not(:where([class~="not-prose"] *)) {
  color: var(--tw-prose-links);
  text-decoration: none;
  font-weight: 500;
  transition: all 0.2s ease;
}

.prose :where(a):not(:where([class~="not-prose"] *)):hover {
  text-decoration: underline;
  color: theme('colors.indigo.700');
}

.prose :where(blockquote):not(:where([class~="not-prose"] *)) {
  font-style: italic;
  border-left: 4px solid var(--tw-prose-quote-borders);
  padding-left: 1em;
  margin-top: 1.5em;
  margin-bottom: 1.5em;
  color: var(--tw-prose-quotes);
}

.prose :where(code):not(:where([class~="not-prose"] *)) {
  background-color: theme('colors.slate.100');
  padding: 0.125rem 0.375rem;
  border-radius: 0.375rem;
  font-size: 0.875em;
  font-weight: 600;
  color: theme('colors.slate.900');
}

.prose :where(pre):not(:where([class~="not-prose"] *)) {
  background-color: theme('colors.slate.800');
  color: theme('colors.slate.100');
  padding: 1rem;
  border-radius: 0.75rem;
  overflow-x: auto;
  margin-top: 1.5em;
  margin-bottom: 1.5em;
}

.prose :where(pre code):not(:where([class~="not-prose"] *)) {
  background-color: transparent;
  padding: 0;
  color: inherit;
  font-weight: 400;
}

.prose :where(h1, h2, h3, h4, h5, h6):not(:where([class~="not-prose"] *)) {
  color: var(--tw-prose-headings);
  font-weight: 700;
  margin-top: 1.5em;
  margin-bottom: 0.75em;
}

.prose :where(p):not(:where([class~="not-prose"] *)) {
  margin-top: 1em;
  margin-bottom: 1em;
  line-height: 1.7;
}

/* Custom scrollbar for modal */
.overflow-y-auto::-webkit-scrollbar {
  width: 6px;
}

.overflow-y-auto::-webkit-scrollbar-track {
  background: theme('colors.slate.100');
  border-radius: 3px;
}

.overflow-y-auto::-webkit-scrollbar-thumb {
  background: theme('colors.slate.300');
  border-radius: 3px;
}

.overflow-y-auto::-webkit-scrollbar-thumb:hover {
  background: theme('colors.slate.400');
}

/* Smooth transitions for interactive elements */
* {
  transition-property: color, background-color, border-color, text-decoration-color, fill, stroke, opacity, box-shadow, transform, filter, backdrop-filter;
  transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);
  transition-duration: 150ms;
}
</style>