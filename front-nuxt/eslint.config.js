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
    ignores: ['packages-legacy/**'],
  },
  {
    files: ['docs/**/*.vue'],
    rules: {
      'vue/no-v-html': 'off',
    },
  },
)
