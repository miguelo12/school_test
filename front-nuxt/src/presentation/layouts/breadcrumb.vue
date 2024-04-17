<script setup>
function getBreadcrumItems() {
  const fullPath = useRoute().fullPath
  const pathArray = fullPath.substring(1).split('/')
  const breadcrumbItems = [{
    title: 'index',
    disabled: false,
    goto: `/`,
  }]

  let pathBuild = ''
  pathArray.forEach((element) => {
    pathBuild += '/' + element
    breadcrumbItems.push({
      title: element,
      disabled: useRoute().name?.toString() == element,
      goto: `${pathBuild}`,
    })
  })
  return breadcrumbItems
}
</script>

<template>
  <v-breadcrumbs
    class="text-primary text-capitalize"
    :items="getBreadcrumItems()"
  >
    <template
      #title="{ item }"
    >
      <NuxtLink
        class="text-primay cursor-pointer"
        :to="!item.disabled ? item.goto : ''"
      >
        {{ item.title }}
      </NuxtLink>
    </template>
  </v-breadcrumbs>
</template>
