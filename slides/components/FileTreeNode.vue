<script setup lang="ts">
import { computed } from 'vue'

type Node = {
  name: string
  type?: 'dir' | 'file' | 'link'
  target?: string
  comment?: string
  children?: Node[]
}

const props = defineProps<{
  node: Node
  // For each ancestor level, true means a vertical line passes through
  // this column (because that ancestor still has more siblings below);
  // false means the column is empty (ancestor's branch has terminated).
  ancestorsHasMore: boolean[]
  isLast: boolean
}>()

const childAncestors = computed(() => [...props.ancestorsHasMore, !props.isLast])
</script>

<template>
  <div class="row">
    <!-- One gutter per ancestor level: draws a vertical line if that
         level still has more siblings, otherwise an empty spacer. -->
    <span
      v-for="(hasMore, i) in ancestorsHasMore"
      :key="i"
      class="gutter"
      :class="{ 'gutter--vert': hasMore }"
    />
    <!-- Elbow gutter for this row: vertical-stub + horizontal stub.
         For non-last rows it's the ├ shape; last rows the └ shape. -->
    <span class="gutter elbow" :class="{ 'elbow--last': isLast }">
      <span class="elbow-h" />
    </span>
    <carbon-folder    v-if="node.type === 'dir'"       class="icon dir" />
    <carbon-link      v-else-if="node.type === 'link'" class="icon link" />
    <carbon-document  v-else                            class="icon file" />
    <span :class="['name', node.type || 'file']">{{ node.name }}</span>
    <span v-if="node.target" class="target">  →  {{ node.target }}</span>
    <span v-if="node.comment" class="comment">    # {{ node.comment }}</span>
  </div>
  <FileTreeNode
    v-for="(child, i) in node.children || []"
    :key="i"
    :node="child"
    :ancestors-has-more="childAncestors"
    :is-last="i === (node.children!.length - 1)"
  />
</template>
