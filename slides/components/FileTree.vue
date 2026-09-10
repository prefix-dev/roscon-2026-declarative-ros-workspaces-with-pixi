<script setup lang="ts">
import FileTreeNode from './FileTreeNode.vue'

type Node = {
  name: string
  type?: 'dir' | 'file' | 'link'
  target?: string
  comment?: string
  children?: Node[]
}

defineProps<{ tree: Node[]; rootLabel?: string }>()
</script>

<template>
  <div class="file-tree">
    <div v-if="rootLabel" class="row root">
      <carbon-folder class="icon dir" />
      <span class="name dir">{{ rootLabel }}</span>
    </div>
    <FileTreeNode
      v-for="(node, i) in tree"
      :key="i"
      :node="node"
      :ancestors-has-more="[]"
      :is-last="i === tree.length - 1"
    />
  </div>
</template>

<style scoped>
.file-tree {
  font-family: 'JetBrains Mono', ui-monospace, monospace;
  font-size: 1rem;
  line-height: 1.5;
  color: var(--prefix-navy);
  --gutter-w: 1.4em;
  --rule-color: rgb(0 24 56 / 55%);
}
.file-tree :deep(.row) {
  display: flex;
  align-items: center;
  position: relative;
}
/* Gutter columns: one per ancestor depth + the row's own elbow. They
 * are drawn as flex children of fixed width, with continuous vertical
 * lines via top/bottom borders that span the full row height. This
 * way verticals on consecutive rows touch regardless of line-height. */
.file-tree :deep(.gutter) {
  flex: 0 0 var(--gutter-w);
  align-self: stretch;
  position: relative;
}
/* Vertical line passing fully through this gutter. */
.file-tree :deep(.gutter--vert)::before {
  content: '';
  position: absolute;
  top: 0;
  bottom: 0;
  left: 0.35em;
  width: 0;
  border-left: 1px solid var(--rule-color);
}
/* The row's own elbow: vertical line from row top to vertical centre,
 * plus a horizontal stub reaching the icon. */
.file-tree :deep(.elbow)::before {
  content: '';
  position: absolute;
  top: 0;
  /* default: ├: line goes from top through the full row */
  bottom: 0;
  left: 0.35em;
  width: 0;
  border-left: 1px solid var(--rule-color);
}
.file-tree :deep(.elbow--last)::before {
  /* └: line stops at the row's vertical centre */
  bottom: 50%;
}
.file-tree :deep(.elbow-h) {
  position: absolute;
  top: 50%;
  left: 0.35em;
  width: 0.85em;
  height: 0;
  border-top: 1px solid var(--rule-color);
}
.file-tree :deep(.icon) {
  flex-shrink: 0;
  width: 0.95rem;
  height: 0.95rem;
  margin-right: 0.4rem;
}
.file-tree :deep(.icon.dir)  { color: var(--prefix-yellow); }
.file-tree :deep(.icon.file) { color: var(--prefix-navy); }
.file-tree :deep(.icon.link) { color: var(--prefix-blue); }
.file-tree :deep(.name)      { font-weight: 500; }
.file-tree :deep(.name.dir)  { color: var(--prefix-navy); }
.file-tree :deep(.name.link) { color: var(--prefix-blue); }
.file-tree :deep(.name.file) { color: var(--prefix-navy); }
.file-tree :deep(.target)    { color: var(--prefix-blue); font-style: italic; }
.file-tree :deep(.comment)   { color: rgb(0 24 56 / 55%); font-style: italic; margin-left: 0.6em; }
.file-tree .root .name       { color: var(--prefix-navy); font-weight: 500; }
</style>
