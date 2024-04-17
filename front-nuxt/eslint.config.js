import { createConfigForNuxt } from '@nuxt/eslint-config/flat'

export default createConfigForNuxt({
  features: {
    stylistic: true,
    tooling: true,
  },
  dirs: {
    src: ['playground', 'docs'],
  },
}).append(
  {
    rules: { 'vue/multi-word-component-names': 'off' },
  },
  {
    rules: { 'vue/valid-v-slot': ['error', {
      allowModifiers: true,
    }] },
  },
  {
    ignores: ['packages-legacy/**'],
  },
  {
    files: ['docs/**/*.vue'],
    rules: {
      'vue/no-v-html': 'off',
    },
  },
)
