<template>
  <v-container class="fill-height">
    <v-row align="center" justify="center">
      <v-col cols="12" md="6" class="text-center">
        <v-icon size="200" color="grey">mdi-alert-circle-outline</v-icon>
        <h1 class="text-h2 font-weight-bold mb-4">404</h1>
        <h2 class="text-h4 mb-4">Page Not Found</h2>
        <p class="text-body-1 text-medium-emphasis mb-6">
          The page you're looking for doesn't exist or has been moved.
        </p>
        <v-btn
          color="primary"
          size="large"
          prepend-icon="mdi-home"
          to="/dashboard"
        >
          Go to Dashboard
        </v-btn>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
export default {
  name: 'NotFound'
}
</script>
