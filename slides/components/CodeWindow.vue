<script setup lang="ts">
defineProps<{
  title: string
  terminal?: boolean
  /** Whole-window size as a percentage; defaults to 100. */
  scale?: number
}>()
</script>

<template>
  <div class="code-window" :class="{ 'code-window--terminal': terminal }" :style="{ zoom: (scale ?? 100) / 100 }" role="group" :aria-label="title">
    <div class="window-bar">
      <span v-if="terminal" class="window-controls" aria-hidden="true">
        <span class="window-dot window-dot--red"></span>
        <span class="window-dot window-dot--yellow"></span>
        <span class="window-dot window-dot--green"></span>
      </span>
      <svg v-else class="window-file" aria-hidden="true" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.2" stroke-linejoin="round">
        <path d="M3.5 1.5h5.2L12.5 5.3v9.2a.5.5 0 0 1-.5.5H3.5a.5.5 0 0 1-.5-.5V2a.5.5 0 0 1 .5-.5z" />
        <path d="M8.6 1.6V5.4H12.4" />
      </svg>
      <span class="window-title">{{ title }}</span>
    </div>
    <div class="window-body">
      <slot />
    </div>
  </div>
</template>

<style scoped>
.code-window {
  min-width: 0;
  align-self: start;
  margin-bottom: 0.75rem;
  text-align: left;
  overflow: hidden;
  border: 1px solid rgb(0 24 56 / 12%);
  border-radius: 8px;
  background: #edeae4;
  box-shadow: 0 6px 18px rgb(0 24 56 / 6%);
}

.window-bar {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.55rem 0.85rem;
  border-bottom: 1px solid rgb(0 24 56 / 10%);
  background: rgb(0 24 56 / 4%);
  color: var(--prefix-navy);
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.85rem;
  line-height: 1.4;
}

.code-window--terminal .window-bar {
  background: rgb(255 212 50 / 12%);
}

.window-file {
  width: 1rem;
  height: 1rem;
  flex-shrink: 0;
}

.window-controls {
  display: flex;
  gap: 0.35rem;
}

.window-dot {
  width: 0.6rem;
  height: 0.6rem;
  border-radius: 50%;
}

.window-dot--red { background: var(--prefix-red); }
.window-dot--yellow { background: var(--prefix-yellow); }
.window-dot--green { background: var(--prefix-green); }

.code-window--terminal .window-title {
  flex: 1;
  text-align: center;
  margin-right: 2.5rem;
}

.window-body :deep(pre) {
  margin: 0;
  padding: 0.85rem !important;
  border-radius: 0;
  white-space: pre-wrap;
  overflow-wrap: anywhere;
}
</style>
