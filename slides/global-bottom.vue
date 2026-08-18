<template>
  <div class="slide-footer">
    <div class="footer-left">
      <img src="/prefix-logo.svg" alt="prefix.dev" class="footer-logo" />
      <span class="footer-title">ROSCon 2026</span>
    </div>
    <div class="footer-center">
      <span
        v-if="$slidev.nav.currentSlideRoute?.meta?.slide?.frontmatter?.section"
        class="footer-section"
      >
        {{ $slidev.nav.currentSlideRoute.meta.slide.frontmatter.section }}
      </span>
    </div>
    <div class="footer-right">
      <span class="footer-page">{{ $nav.currentPage }} / {{ $nav.total }}</span>
    </div>
  </div>
</template>

<style scoped>
.slide-footer {
  position: fixed;
  bottom: 12px;
  left: 24px;
  right: 24px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  opacity: 0.5;
  z-index: 10;
  pointer-events: none;
}

.footer-left {
  display: flex;
  align-items: center;
  gap: 8px;
  flex: 1;
}

.footer-center {
  flex: 1;
  display: flex;
  justify-content: center;
}

.footer-right {
  flex: 1;
  display: flex;
  justify-content: flex-end;
}

.footer-logo {
  height: 20px;
  width: auto;
}

.footer-title,
.footer-page {
  font-family: 'Inter', sans-serif;
  font-size: 11px;
  font-weight: 500;
  color: currentColor;
}

.footer-section {
  font-family: 'Inter', sans-serif;
  font-size: 11px;
  font-weight: 600;
  color: currentColor;
  padding: 1px 8px;
  border: 1px solid currentColor;
  border-radius: 4px;
}
</style>
