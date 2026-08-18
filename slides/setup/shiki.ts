import { defineShikiSetup } from '@slidev/types'

// Code blocks in the prefix.dev colours, matching style.css:
//   navy   #001838  plain text
//   blue   #5773ff  keys, commands, table headers
//   green  #70c038  strings, arguments
//   red    #ff6a38  numbers, booleans, flags
// Yellow (#ffd432) is left out: no contrast on the off-white background.
const prefixLight = {
  name: 'prefix-light',
  type: 'light' as const,
  colors: {
    'editor.background': '#edeae4',
    'editor.foreground': '#001838',
  },
  settings: [
    { settings: { foreground: '#001838' } },
    {
      scope: ['comment', 'punctuation.definition.comment'],
      settings: { foreground: '#001838a6', fontStyle: 'italic' },
    },
    {
      scope: [
        'string',
        'string.quoted',
        'punctuation.definition.string',
        'meta.embedded.assembly',
      ],
      settings: { foreground: '#4f8f22' },
    },
    {
      scope: [
        'keyword',
        'storage',
        'entity.name.tag',
        'entity.name.function',
        'support.function',
        'support.type.property-name',
        'variable.other.constant',
        'entity.name.section',
        'entity.name.tag.toml',
        'entity.name.tag.table.toml',
        'entity.name.tag.table.array.toml',
        'support.type.property-name.table.toml',
        'support.type.property-name.toml',
        'keyword.key.toml',
        'entity.name.tag.yaml',
      ],
      settings: { foreground: '#5773ff' },
    },
    {
      scope: [
        'constant.numeric',
        'constant.language',
        'constant.other',
        'variable.parameter',
        'keyword.operator',
        'entity.name.type',
        'support.type',
      ],
      settings: { foreground: '#ff6a38' },
    },
    {
      // Shell: the command name is blue, its arguments navy
      scope: ['entity.name.command', 'support.function.builtin.shell', 'entity.name.function.call.shell'],
      settings: { foreground: '#5773ff' },
    },
    {
      scope: ['variable', 'variable.other', 'meta.function-call.arguments'],
      settings: { foreground: '#001838' },
    },
    {
      // Table headers in console output, `$` prompt
      scope: ['punctuation.definition.variable', 'punctuation.separator', 'meta.brace', 'punctuation.definition.table'],
      settings: { foreground: '#001838' },
    },
  ],
}

export default defineShikiSetup(() => {
  return {
    themes: {
      light: prefixLight,
      dark: prefixLight,
    },
  }
})
