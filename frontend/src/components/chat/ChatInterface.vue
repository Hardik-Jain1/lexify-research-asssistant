<template>
    <div class="flex flex-col h-full bg-white/95 backdrop-blur-sm shadow-2xl rounded-2xl border border-slate-200/60 overflow-hidden">
        <!-- Header with Gradient -->
        <header class="relative overflow-hidden bg-gradient-to-r from-indigo-600 via-purple-600 to-indigo-700 p-6">
            <div class="absolute inset-0 bg-gradient-to-br from-white/10 to-transparent"></div>
            <div class="relative">
                <div class="flex items-center justify-between">
                    <div class="flex items-center space-x-3">
                        <div class="w-3 h-3 bg-emerald-400 rounded-full shadow-lg shadow-emerald-200"></div>
                        <h2 class="text-xl font-bold text-white">
                            Research Chat
                        </h2>
                    </div>
                    <div class="bg-white/20 backdrop-blur-sm px-3 py-1 rounded-full">
                        <span class="text-white text-sm font-medium">
                            {{ selectedPaperIds.length }} paper{{ selectedPaperIds.length !== 1 ? 's' : '' }}
                        </span>
                    </div>
                </div>
                <p v-if="selectedPaperTitles.length" class="text-white/80 text-sm mt-2 truncate">
                    {{ selectedPaperTitles.join(' • ') }}
                </p>
            </div>
        </header>

        <!-- Messages Area -->
        <div ref="messageContainer" class="flex-grow p-6 space-y-6 overflow-y-auto bg-gradient-to-br from-slate-50 via-white to-indigo-50/30 custom-scrollbar">
            <!-- Empty State -->
            <div v-if="!messages.length" class="flex flex-col items-center justify-center h-full text-center py-12">
                <div class="relative mb-6">
                    <div class="absolute inset-0 bg-gradient-to-r from-indigo-400/20 to-purple-400/20 rounded-full blur-3xl transform scale-150"></div>
                    <div class="relative bg-gradient-to-br from-indigo-100 to-purple-100 p-8 rounded-3xl shadow-inner">
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-12 h-12 text-indigo-600 mx-auto">
                            <path stroke-linecap="round" stroke-linejoin="round" d="M8.625 12a.375.375 0 1 1-.75 0 .375.375 0 0 1 .75 0Zm0 0H8.25m4.125 0a.375.375 0 1 1-.75 0 .375.375 0 0 1 .75 0Zm0 0H12m4.125 0a.375.375 0 1 1-.75 0 .375.375 0 0 1 .75 0Zm0 0h-.375M21 12c0 4.556-4.03 8.25-9 8.25a9.764 9.764 0 0 1-2.555-.337A5.972 5.972 0 0 1 5.41 20.97a5.969 5.969 0 0 1-.474-.065 4.48 4.48 0 0 0 .978-2.025c.09-.457-.133-.901-.467-1.226C3.93 16.178 3 14.189 3 12c0-4.556 4.03-8.25 9-8.25s9 3.694 9 8.25Z" />
                        </svg>
                    </div>
                </div>
                <h3 class="text-xl font-semibold text-slate-700 mb-2">Start Your Research Conversation</h3>
                <p class="text-slate-500 max-w-md">Ask questions about your selected papers to uncover insights, compare findings, or explore connections between research.</p>
            </div>

            <!-- Messages -->
            <div v-for="(message, index) in messages" :key="index" :class="messageBubbleClass(message.role)">
                <div :class="messageContentClass(message.role)">
                    <!-- Message Content -->
                    <div v-if="message.role === 'assistant'" class="prose prose-sm max-w-none prose-slate" v-html="renderMarkdown(message.content)"></div>
                    <p v-else class="text-sm whitespace-pre-line leading-relaxed">{{ message.content }}</p>
                    
                    <!-- Sources Section -->
                    <div v-if="message.role === 'assistant' && message.sources && Object.keys(message.sources).length > 0" class="mt-4 pt-3 border-t border-slate-200/50">
                        <div class="flex items-center mb-2">
                            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-4 h-4 mr-2 text-indigo-500">
                                <path stroke-linecap="round" stroke-linejoin="round" d="M12 6.042A8.967 8.967 0 0 0 6 3.75c-1.052 0-2.062.18-3 .512v14.25A8.987 8.987 0 0 1 6 18c2.305 0 4.408.867 6 2.292m0-14.25a8.966 8.966 0 0 1 6-2.292c1.052 0 2.062.18 3 .512v14.25A8.987 8.987 0 0 1 18 18a8.967 8.967 0 0 0-6 2.292m0-14.25v14.25" />
                            </svg>
                            <span class="text-xs font-semibold text-slate-600 uppercase tracking-wide">Referenced Sources</span>
                        </div>
                        <div class="space-y-2">
                            <div v-for="(source, key) in message.sources" :key="key"
                                class="group p-3 rounded-lg bg-white/60 border border-slate-200/60 hover:bg-indigo-50/60 hover:border-indigo-200 cursor-pointer transition-all duration-200"
                                :title="`Source: ${source.title || key}\nContext: ${source.text}`"
                                @click="handleSourceClick(source, key as string)">
                                <div class="flex items-start space-x-2">
                                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16" fill="currentColor" class="w-4 h-4 mt-0.5 text-indigo-500 group-hover:text-indigo-600 transition-colors">
                                        <path d="M3.5 2A1.5 1.5 0 0 0 2 3.5v9A1.5 1.5 0 0 0 3.5 14h9a1.5 1.5 0 0 0 1.5-1.5V6.528a1.5 1.5 0 0 0-.44-1.06L9.53 2.439A1.5 1.5 0 0 0 8.472 2H3.5ZM8 6V3.5L12.5 8H9a1 1 0 0 1-1-1Z" />
                                    </svg>
                                    <div class="flex-1 min-w-0">
                                        <p class="text-sm font-medium text-slate-700 group-hover:text-indigo-700 truncate">
                                            {{ source.title || key }}
                                        </p>
                                        <p class="text-xs text-slate-500 mt-1 line-clamp-2">
                                            {{ source.text }}
                                        </p>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- Timestamp -->
                    <p v-if="message.timestamp" class="text-xs text-slate-400 mt-3 text-right opacity-60">
                        {{ formatTimestamp(message.timestamp) }}
                    </p>
                </div>
            </div>

            <!-- Typing Indicator -->
            <div v-if="isLoadingResponse" class="flex justify-start">
                <div class="bg-gradient-to-r from-slate-100 to-slate-200 border border-slate-200/60 p-4 rounded-2xl max-w-xs shadow-sm">
                    <div class="flex items-center space-x-2">
                        <div class="flex space-x-1">
                            <div class="w-2 h-2 bg-slate-400 rounded-full animate-bounce"></div>
                            <div class="w-2 h-2 bg-slate-400 rounded-full animate-bounce" style="animation-delay: 0.1s"></div>
                            <div class="w-2 h-2 bg-slate-400 rounded-full animate-bounce" style="animation-delay: 0.2s"></div>
                        </div>
                        <span class="text-sm text-slate-600">AI is thinking...</span>
                    </div>
                </div>
            </div>
        </div>

        <!-- Input Footer -->
        <footer class="relative bg-white/80 backdrop-blur-sm border-t border-slate-200/60 p-6">
            <div class="absolute inset-0 bg-gradient-to-r from-indigo-50/30 to-purple-50/30"></div>
            <div class="relative">
                <form @submit.prevent="sendMessage" class="flex items-end gap-3">
                    <div class="flex-grow relative">
                        <input
                            type="text"
                            v-model="userInput"
                            placeholder="Ask about your research papers..."
                            :disabled="isLoadingResponse"
                            class="w-full px-4 py-3 border-2 border-slate-200 rounded-xl shadow-sm focus:ring-2 focus:ring-indigo-500/20 focus:border-indigo-400 text-sm transition-all duration-200 bg-white/80 backdrop-blur-sm placeholder-slate-400"
                        />
                        <div class="absolute right-3 top-1/2 -translate-y-1/2">
                            <div class="w-2 h-2 bg-emerald-400 rounded-full animate-pulse"></div>
                        </div>
                    </div>
                    <button
                        type="submit"
                        :disabled="isLoadingResponse || !userInput.trim()"
                        class="group relative inline-flex items-center justify-center px-6 py-3 border border-transparent text-sm font-semibold rounded-xl shadow-lg text-white bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-700 hover:to-purple-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-200 hover:shadow-xl hover:-translate-y-0.5"
                    >
                        <svg v-if="isLoadingResponse" class="animate-spin -ml-1 mr-2 h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                        </svg>
                        <svg v-else xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="w-4 h-4 mr-2 group-hover:translate-x-0.5 transition-transform">
                            <path stroke-linecap="round" stroke-linejoin="round" d="M6 12 3.269 3.125A59.769 59.769 0 0 1 21.485 12 59.768 59.768 0 0 1 3.27 20.875L5.999 12Zm0 0h7.5" />
                        </svg>
                        {{ isLoadingResponse ? 'Sending...' : 'Send' }}
                    </button>
                </form>
                
                <!-- Error Message -->
                <div v-if="chatError" class="mt-3 p-3 bg-red-50 border border-red-200 rounded-lg">
                    <div class="flex items-center">
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-5 h-5 text-red-500 mr-2">
                            <path stroke-linecap="round" stroke-linejoin="round" d="M12 9v3.75m9-.75a9 9 0 1 1-18 0 9 9 0 0 1 18 0Zm-9 3.75h.008v.008H12v-.008Z" />
                        </svg>
                        <p class="text-sm text-red-700">{{ chatError }}</p>
                    </div>
                </div>
            </div>
        </footer>
    </div>
</template>

<script setup lang="ts">
// ... existing script setup ...
import { ref, watch, nextTick, onMounted, computed } from 'vue';
import { marked } from 'marked';
import DOMPurify from 'dompurify';
import * as ragService from '@/services/ragService';
import type { ChatMessage, Paper, ChatMessageSource } from '@/types';

console.log('ChatInterface: script setup started');

const props = defineProps<{
    selectedPaperIds: number[];
    initialMessages?: ChatMessage[];
    initialSessionId?: number | null; // Changed from currentChatSessionId to initialSessionId
    papersInContext: Paper[];
    //isVisible: boolean; // Assuming this might be used if it's a modal controlled by ResearchView
}>();

console.log('ChatInterface props received:', JSON.parse(JSON.stringify(props)));

const emit = defineEmits(['session-updated', 'chat-closed', 'source-clicked']); // chat-closed might be emitted to parent

const messages = ref<ChatMessage[]>(props.initialMessages || []);
const userInput = ref('');
const isLoadingResponse = ref(false);
const chatError = ref<string | null>(null);
const currentChatSessionId = ref<number | null>(props.initialSessionId || null);
const messageContainer = ref<HTMLElement | null>(null);

const selectedPaperTitles = computed(() => {
    console.log('ChatInterface: computing selectedPaperTitles. papersInContext:', props.papersInContext, 'selectedPaperIds:', props.selectedPaperIds);
    if (!props.papersInContext || !Array.isArray(props.papersInContext)) {
        console.error('ChatInterface: papersInContext is invalid', props.papersInContext);
        return [];
    }
    if (!props.selectedPaperIds || !Array.isArray(props.selectedPaperIds)) {
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

const renderMarkdown = (content: string) => {
  if (!content) return '';
  let linkedContent = content.replace(/\[(.*?)\]/g, (match, innerContent) => {
    const ids = innerContent.split(',').map(id => id.trim()).filter(id => id);
    if (ids.length === 0) return match;

    const links = ids.map(paperId => {
      const cleanPaperId = paperId.replace(/[^A-Za-z0-9.-v]/g, '');
      if (!cleanPaperId) return paperId;
      // Ensure prose link styles are applied by Tailwind Typography or custom styles
      return `<a href="#" data-paper-id="${cleanPaperId}" class="font-medium">${paperId}</a>`;
    });
    return `[${links.join(', ')}]`;
  });

  const rawHtml = marked.parse(linkedContent) as string;
  // Ensure data-paper-id is allowed and that links open in new tab if they are external
  return DOMPurify.sanitize(rawHtml, {
    ADD_ATTR: ['data-paper-id'],
    ADD_TAGS: ['a'], // Ensure 'a' tags are allowed
    FORBID_TAGS: [], // Customize if needed
    FORBID_ATTR: [], // Customize if needed
    USE_PROFILES: { html: true }, // Use a broad profile
    ADD_URI_SAFE_ATTR: ['data-paper-id']
  });
};

const handleSourceClick = (source: ChatMessageSource, key: string) => {
    console.log('Source clicked:', source.title || key, source);
    emit('source-clicked', { title: source.title || key, text: source.text, rawSource: source });
};

const scrollToBottom = () => {
    nextTick(() => {
        if (messageContainer.value) {
            messageContainer.value.scrollTop = messageContainer.value.scrollHeight;
        }
    });
};

watch(messages, scrollToBottom, { deep: true });

// Watch for prop changes to reset chat if session or selected papers change significantly
watch(() => [props.initialSessionId, props.selectedPaperIds], ([newSessionId, newSelectedIds], [oldSessionId, oldSelectedIds]) => {
    console.log('ChatInterface: Props changed - initialSessionId or selectedPaperIds');
    // Basic check: if session ID changes, or if selected papers fundamentally change (e.g. from some to none, or all different)
    // More sophisticated logic might be needed depending on desired behavior.
    // For now, if initialSessionId changes, we reset.
    if (newSessionId !== oldSessionId) {
        console.log(`ChatInterface: Resetting due to session ID change. New: ${newSessionId}, Old: ${oldSessionId}`);
        resetChat(newSessionId, []); // Reset with new session ID and clear messages
    }
    // Potentially add logic here if selectedPaperIds change and you want to start a new session or clear messages.
}, { deep: true });


const setupCitationClickListener = () => {
  if (messageContainer.value) {
    messageContainer.value.addEventListener('click', (event) => {
      const target = event.target as HTMLElement;
      if (target.tagName === 'A' && target.hasAttribute('data-paper-id')) {
        event.preventDefault();
        const paperId = target.getAttribute('data-paper-id');
        console.log('Inline citation clicked:', paperId);
        // Placeholder for future: emit('citation-clicked', paperId);
        alert(`Citation clicked: ${paperId}`);
      }
    });
  }
};

onMounted(async () => {
    console.log('ChatInterface: component mounted. Initial session ID:', props.initialSessionId);
    if (props.initialSessionId) {
        currentChatSessionId.value = props.initialSessionId;
        // Fetch initial messages if a session ID is provided
        isLoadingResponse.value = true;
        try {
            const existingMessages = await ragService.getChatSessionMessages(props.initialSessionId);
            messages.value = existingMessages.messages; // Assuming the service returns { messages: ChatMessage[] }
            emit('session-updated', props.initialSessionId); // Confirm session
        } catch (error) {
            console.error('Failed to load messages for session:', props.initialSessionId, error);
            chatError.value = "Failed to load previous session messages.";
        } finally {
            isLoadingResponse.value = false;
            scrollToBottom();
        }
    } else {
        messages.value = []; // Start with no messages if no session ID
    }
    scrollToBottom();
    setupCitationClickListener();
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
    userInput.value = '';
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
         if (!currentChatSessionId.value && response.chat_session_id) { // First message in a new session
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
    let baseClass = 'p-4 rounded-2xl max-w-2xl shadow-lg text-sm backdrop-blur-sm border';
    if (role === 'user') {
        return `${baseClass} bg-gradient-to-br from-indigo-600 to-purple-600 text-white border-indigo-500/30 shadow-indigo-200`;
    }
    return `${baseClass} bg-white/80 text-slate-800 border-slate-200/60`;
};

const formatTimestamp = (isoString?: string) => {
    if (!isoString) return '';
    return new Date(isoString).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
};

const resetChat = (newSessionId: number | null = null, newMessages: ChatMessage[] = []) => {
    console.log(`ChatInterface: resetChat called. New session ID: ${newSessionId}`);
    messages.value = [...newMessages]; // Ensure reactivity by creating a new array
    currentChatSessionId.value = newSessionId;
    chatError.value = null;
    isLoadingResponse.value = false; // Ensure loading state is reset
    userInput.value = ''; // Clear user input
    scrollToBottom();
};

defineExpose({ resetChat });

</script>

<style scoped>
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

.line-clamp-2 {
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
}

/* Custom Scrollbar for Webkit browsers */
.custom-scrollbar::-webkit-scrollbar {
    width: 6px;
}
.custom-scrollbar::-webkit-scrollbar-track {
    background: transparent;
}
.custom-scrollbar::-webkit-scrollbar-thumb {
    background: theme('colors.slate.300');
    border-radius: 3px;
}
.custom-scrollbar::-webkit-scrollbar-thumb:hover {
    background: theme('colors.slate.400');
}

/* Enhanced Prose styles for Markdown content */
.prose :where(a):not(:where([class~="not-prose"] *)) {
  color: theme('colors.indigo.600');
  text-decoration: none;
  font-weight: 500;
  padding: 2px 4px;
  border-radius: 4px;
  transition: all 0.2s ease;
}
.prose :where(a):not(:where([class~="not-prose"] *)):hover {
  background-color: theme('colors.indigo.50');
  text-decoration: underline;
  color: theme('colors.indigo.700');
}
.prose :where(ul):not(:where([class~="not-prose"] *)) {
  list-style-type: disc;
  padding-left: 1.5em;
  margin: 1em 0;
}
.prose :where(ol):not(:where([class~="not-prose"] *)) {
  list-style-type: decimal;
  padding-left: 1.5em;
  margin: 1em 0;
}
.prose :where(strong):not(:where([class~="not-prose"] *)) {
  font-weight: 600;
  color: theme('colors.slate.900');
}
.prose :where(p):not(:where([class~="not-prose"] *)) {
  margin: 0.75em 0;
  line-height: 1.6;
}
.prose :where(blockquote):not(:where([class~="not-prose"] *)) {
  border-left: 4px solid theme('colors.indigo.300');
  padding-left: 1em;
  margin: 1em 0;
  background-color: theme('colors.indigo.50');
  border-radius: 0 8px 8px 0;
  padding: 1em;
}
.prose :where(code):not(:where([class~="not-prose"] *)) {
  background-color: theme('colors.slate.100');
  padding: 2px 4px;
  border-radius: 4px;
  font-family: theme('fontFamily.mono');
  font-size: 0.875em;
  font-weight: 500;
}
</style>