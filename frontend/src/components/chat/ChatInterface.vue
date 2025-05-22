<template>
  <div class="flex flex-col h-full bg-white shadow-xl rounded-lg border border-gray-200">
    <header class="p-4 border-b border-gray-200 bg-gray-50 rounded-t-lg">
      <h2 class="text-lg font-semibold text-gray-700">
        Chat with Selected Papers ({{ selectedPaperIds.length }} paper<span v-if="selectedPaperIds.length !== 1">s</span>)
      </h2>
      <p v-if="selectedPaperTitles.length" class="text-xs text-gray-500 truncate">
        Papers: {{ selectedPaperTitles.join(', ') }}
      </p>
    </header>

    <div ref="messageContainer" class="flex-grow p-4 space-y-4 overflow-y-auto bg-gray-100">
      <div v-if="!messages.length" class="text-center text-gray-500 pt-10">
        <p>Ask a question about the selected papers to start the conversation.</p>
      </div>
      <div v-for="(message, index) in messages" :key="index" :class="messageBubbleClass(message.role)">
        <div :class="messageContentClass(message.role)">
          <p class="text-sm whitespace-pre-line">{{ message.content }}</p>
          <div v-if="message.role === 'assistant' && message.sources && Object.keys(message.sources).length > 0" class="mt-2 text-xs text-gray-500">
            <strong class="text-gray-600">Sources:</strong>
            <ul class="list-disc list-inside ml-2">
              <li v-for="(source, key) in message.sources" :key="key" :title="`Context: ${source.text}`" class="truncate hover:whitespace-normal">
                {{ source.title || key }}
              </li>
            </ul>
          </div>
          <p v-if="message.timestamp" class="text-xs text-gray-400 mt-1 text-right">{{ formatTimestamp(message.timestamp) }}</p>
        </div>
      </div>
      <div v-if="isLoadingResponse" class="flex justify-start">
        <div class="bg-gray-200 text-gray-700 p-3 rounded-lg max-w-xl animate-pulse">
          <p class="text-sm">Assistant is typing...</p>
        </div>
      </div>
    </div>

    <footer class="p-4 border-t border-gray-200 bg-gray-50 rounded-b-lg">
      <form @submit.prevent="sendMessage" class="flex items-center gap-3">
        <input
          type="text"
          v-model="userInput"
          placeholder="Ask a question..."
          :disabled="isLoadingResponse"
          class="flex-grow w-full px-4 py-2.5 border border-gray-300 rounded-lg shadow-sm focus:ring-indigo-500 focus:border-indigo-500 text-sm"
        />
        <button
          type="submit"
          :disabled="isLoadingResponse || !userInput.trim()"
          class="inline-flex items-center justify-center px-5 py-2.5 border border-transparent text-sm font-medium rounded-lg shadow-sm text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-60 disabled:cursor-not-allowed"
        >
          <svg v-if="isLoadingResponse" class="animate-spin -ml-1 mr-2 h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
          Send
        </button>
      </form>
      <p v-if="chatError" class="mt-2 text-xs text-red-600">{{ chatError }}</p>
    </footer>
  </div>
</template>

<script setup lang="ts">
import { ref, watch, nextTick, defineProps, defineEmits, onMounted, computed } from 'vue';
import * as ragService from '@/services/ragService';
import type { ChatMessage, Paper } from '@/types';

console.log('ChatInterface: script setup started'); // Add this temprory

const props = defineProps<{
  selectedPaperIds: number[];
  initialMessages?: ChatMessage[]; // For resuming a chat
  initialSessionId?: number | null; // For resuming a chat
  papersInContext: Paper[]; // To display titles
}>();

console.log('ChatInterface props received:', JSON.parse(JSON.stringify(props))); // temporary

const emit = defineEmits(['session-updated', 'chat-closed']); // session-updated can pass new session_id

const messages = ref<ChatMessage[]>(props.initialMessages || []);
const userInput = ref('');
const isLoadingResponse = ref(false);
const chatError = ref<string | null>(null);
const currentChatSessionId = ref<number | null>(props.initialSessionId || null);
const messageContainer = ref<HTMLElement | null>(null);

// const selectedPaperTitles = computed(() => {
//   return props.papersInContext
//     .filter(p => props.selectedPaperIds.includes(p.db_id))
//     .map(p => p.title);
// });
const selectedPaperTitles = computed(() => {
  console.log('ChatInterface: computing selectedPaperTitles. papersInContext:', props.papersInContext, 'selectedPaperIds:', props.selectedPaperIds);
  if (!props.papersInContext || !Array.isArray(props.papersInContext)) { // Defensive check
    console.error('ChatInterface: papersInContext is invalid', props.papersInContext);
    return [];
  }
  if (!props.selectedPaperIds || !Array.isArray(props.selectedPaperIds)) { // Defensive check
    console.error('ChatInterface: selectedPaperIds is invalid', props.selectedPaperIds);
    return [];
  }
  try {
    return props.papersInContext
      .filter(p => props.selectedPaperIds.includes(p.db_id))
      .map(p => p.title);
  } catch (e) {
    console.error('ChatInterface: Error computing selectedPaperTitles', e);
    return [];
  }
});

const scrollToBottom = () => {
  nextTick(() => {
    if (messageContainer.value) {
      messageContainer.value.scrollTop = messageContainer.value.scrollHeight;
    }
  });
};

watch(messages, scrollToBottom, { deep: true });
// onMounted(scrollToBottom);
onMounted(() => {
  console.log('ChatInterface: component mounted'); // Add this
  scrollToBottom();
});


const sendMessage = async () => {
  if (!userInput.value.trim() || isLoadingResponse.value) return;

  const userMessage: ChatMessage = {
    role: 'user',
    content: userInput.value,
    timestamp: new Date().toISOString(),
  };
  messages.value.push(userMessage);
  const currentQuery = userInput.value;
  userInput.value = ''; // Clear input
  isLoadingResponse.value = true;
  chatError.value = null;
  scrollToBottom();

  try {
    const response = await ragService.getChatResponse(
      currentQuery,
      props.selectedPaperIds,
      currentChatSessionId.value
    );

    const assistantMessage: ChatMessage = {
      role: 'assistant',
      content: response.response,
      sources: response.sources,
      timestamp: new Date().toISOString(),
    };
    messages.value.push(assistantMessage);

    if (response.chat_session_id && currentChatSessionId.value !== response.chat_session_id) {
      currentChatSessionId.value = response.chat_session_id;
      emit('session-updated', currentChatSessionId.value);
    }
  } catch (error: any) {
    console.error('Error getting chat response:', error);
    chatError.value = error.response?.data?.msg || error.message || 'Failed to get response from assistant.';
    messages.value.push({
      role: 'assistant',
      content: `Sorry, I encountered an error: ${chatError.value}`,
      timestamp: new Date().toISOString(),
    });
  } finally {
    isLoadingResponse.value = false;
    scrollToBottom();
  }
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

// Expose a method to reset the chat if needed when papers change, etc.
// This might be called by the parent if selected papers change drastically.
const resetChat = (newSessionId: number | null = null, newMessages: ChatMessage[] = []) => {
  messages.value = [...newMessages];
  currentChatSessionId.value = newSessionId;
  chatError.value = null;
  isLoadingResponse.value = false;
  scrollToBottom();
};

defineExpose({ resetChat });

</script>

<style scoped>
/* Ensure the chat interface takes up available height if parent constrains it */
.h-full {
  height: 100%;
}
.truncate {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
.hover\:whitespace-normal:hover {
  white-space: normal;
}
</style>