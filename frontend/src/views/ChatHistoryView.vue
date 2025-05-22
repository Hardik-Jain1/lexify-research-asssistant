<template>
  <div class="container mx-auto p-4 sm:p-6 lg:p-8">
    <h1 class="text-3xl font-bold text-gray-800 mb-8 text-center">Chat History</h1>

    <div v-if="isLoading" class="text-center py-10">
      <div class="inline-block animate-spin rounded-full h-12 w-12 border-t-4 border-b-4 border-indigo-600"></div>
      <p class="mt-4 text-lg text-gray-600">Loading chat sessions...</p>
    </div>

    <div v-if="error" class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded-md relative mb-6" role="alert">
      <strong class="font-bold">Error: </strong>
      <span class="block sm:inline">{{ error }}</span>
    </div>

    <div v-if="!isLoading && !error && sessions.length === 0" class="text-center text-gray-500 py-10 bg-white shadow-lg rounded-lg p-6">
      <p class="text-xl">No chat history found.</p>
      <p class="mt-2">Start a new chat from the Research page to see it listed here.</p>
    </div>

    <div v-if="!isLoading && sessions.length > 0" class="space-y-6">
      <div v-for="session in sessions" :key="session.id" 
           class="bg-white shadow-lg rounded-lg p-6 border border-gray-200 hover:shadow-xl transition-shadow duration-200 cursor-pointer"
           @click="selectSession(session.id)">
        <div class="flex flex-col sm:flex-row justify-between sm:items-center mb-3">
          <h2 class="text-xl font-semibold text-indigo-700 mb-2 sm:mb-0 truncate" :title="session.session_name || (session.paper_titles_in_session && session.paper_titles_in_session.length > 0 ? `Session with: ${session.paper_titles_in_session.join(', ')}` : `Session ${session.id}`)">
            {{ session.session_name || (session.paper_titles_in_session && session.paper_titles_in_session.length > 0 ? `Session with: ${session.paper_titles_in_session.join(', ')}` : `Session ${session.id}`) }}
          </h2>
          <span class="text-xs text-gray-500 bg-gray-100 px-2 py-1 rounded-full whitespace-nowrap">{{ formatDate(session.updated_at) }}</span>
        </div>
        <p class="text-sm text-gray-600 mb-1">
          <strong class="font-medium">Session ID:</strong> {{ session.id }}
        </p>
        
        <div class="mt-3">
            <p class="text-xs font-medium text-gray-500 mb-1">Papers in this session ({{ session.paper_titles_in_session?.length || 0 }}):</p>
            <p v-if="session.paper_titles_in_session && session.paper_titles_in_session.length > 0" class="text-xs text-gray-600 truncate" :title="session.paper_titles_in_session.join(', ')">
                {{ session.paper_titles_in_session.join(', ') }}
            </p>
            <p v-else-if="session.paper_ids_in_session && session.paper_ids_in_session.length > 0" class="text-xs text-gray-600">
                IDs: {{ session.paper_ids_in_session.join(', ') }} (Titles not available)
            </p>
            <p v-else class="text-xs text-gray-500 italic">
                No specific papers linked to this session.
            </p>
        </div>
         <p class="text-sm text-gray-500 italic mt-2">
          Click to view messages.
        </p>
      </div>
    </div>

    <!-- Modal for displaying selected chat session messages -->
    <div v-if="selectedSessionData"  class="fixed inset-0 bg-gray-800 bg-opacity-75 flex items-center justify-center z-50 p-4 backdrop-blur-sm"
         @click.self="closeMessagesModal">
      <div class="bg-white w-full max-w-3xl h-[calc(100vh-4rem)] flex flex-col rounded-lg shadow-xl overflow-hidden">
        <header class="p-4 border-b border-gray-200 bg-gray-50 flex justify-between items-center">
          <h3 class="text-lg font-semibold text-gray-700">
            {{ selectedSessionData.session_name || (selectedSessionData.associated_paper_titles && selectedSessionData.associated_paper_titles.length > 0 ? `Chat with: ${selectedSessionData.associated_paper_titles.join(', ')}` : `Chat Details (Session: ${selectedSessionData.session_id})`) }}
          </h3>
          <button @click="closeMessagesModal" class="text-gray-500 hover:text-gray-700">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
              <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </header>
        
        <div v-if="isLoadingMessages" class="flex-grow flex items-center justify-center">
          <div class="inline-block animate-spin rounded-full h-10 w-10 border-t-4 border-b-4 border-indigo-600"></div>
        </div>
        <div v-if="messagesError" class="p-4 text-red-600 text-center">{{ messagesError }}</div>
        
        <div v-if="selectedSessionData && selectedSessionData.associated_paper_titles && selectedSessionData.associated_paper_titles.length > 0" class="p-3 border-b border-gray-200 bg-gray-50 text-xs text-gray-600">
            <strong>Papers in this session:</strong> {{ selectedSessionData.associated_paper_titles.join(', ') }}
        </div>

        <div v-if="!isLoadingMessages && selectedSessionData && selectedSessionData.messages.length > 0" ref="messageContainerModal" class="flex-grow p-4 space-y-4 overflow-y-auto bg-gray-100">
          <div v-for="(message, index) in selectedSessionData.messages" :key="message.id || index" :class="messageBubbleClass(message.role)">
            <div :class="messageContentClass(message.role)">
              <div v-if="message.role === 'assistant'" class="prose prose-sm max-w-none" v-html="renderMarkdown(message.content)"></div>
              <p v-else class="text-sm whitespace-pre-line">{{ message.content }}</p>
              <div v-if="message.role === 'assistant' && message.sources && Object.keys(message.sources).length > 0" class="mt-3 pt-2 border-t border-gray-300/50 text-xs text-gray-500">
                <strong class="text-gray-600 block mb-1">Sources:</strong>
                <ul class="space-y-1">
                  <li v-for="(source, key) in message.sources" :key="key" 
                      class="truncate hover:whitespace-normal p-1 rounded hover:bg-gray-200/60"
                      :title="`Source: ${source.title || key}\nContext: ${source.text}`">
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16" fill="currentColor" class="w-3 h-3 inline-block mr-1 text-indigo-500">
                      <path d="M3.5 2A1.5 1.5 0 0 0 2 3.5v9A1.5 1.5 0 0 0 3.5 14h9a1.5 1.5 0 0 0 1.5-1.5V6.528a1.5 1.5 0 0 0-.44-1.06L9.53 2.439A1.5 1.5 0 0 0 8.472 2H3.5ZM8 6V3.5L12.5 8H9a1 1 0 0 1-1-1Z" />
                    </svg>
                    {{ source.title || key }}
                  </li>
                </ul>
              </div>
              <p v-if="message.timestamp" class="text-xs text-gray-400 mt-1.5 text-right">{{ formatTimestamp(message.timestamp) }}</p>
            </div>
          </div>
        </div>
        <div v-if="!isLoadingMessages && selectedSessionData && selectedSessionData.messages.length === 0 && !messagesError" class="flex-grow flex items-center justify-center text-gray-500">
            No messages found for this session.
        </div>

        <footer class="p-3 border-t border-gray-200 bg-gray-50 text-center">
          <button @click="resumeChat" 
                  :disabled="!selectedSessionData"
                  class="px-5 py-2.5 bg-green-600 text-white font-medium rounded-lg hover:bg-green-700 focus:ring-4 focus:ring-green-300 transition duration-150 ease-in-out text-sm disabled:opacity-50">
            Resume This Chat
          </button>
        </footer>
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
  let baseClass = 'p-3 rounded-lg max-w-xl shadow-sm text-sm';
  if (role === 'user') {
    return `${baseClass} bg-indigo-500 text-white`;
  }
  return `${baseClass} bg-gray-200 text-gray-800`;
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
/* ... existing styles ... */
.prose :where(ul):not(:where([class~="not-prose"] *)) {
  list-style-type: disc;
  padding-left: 1.5em;
}
.prose :where(strong):not(:where([class~="not-prose"] *)) {
  font-weight: 600;
}
.prose :where(a):not(:where([class~="not-prose"] *)) {
  color: theme('colors.indigo.600'); /* Ensure theme() is available or use direct color */
  text-decoration: none;
}
.prose :where(a):not(:where([class~="not-prose"] *)):hover {
  text-decoration: underline;
}
</style>