<script lang="ts">
    import "toastify-js/src/toastify.css";
    import Navigation from "$lib/nav/Navigation.svelte";
    import "$lib/notify";
</script>

<svelte:head>
    <title>3DC Pro</title>
</svelte:head>

<div class="page page-body my-0">
    <div class="page-header py-3">
        <div class="container-xl">
            <Navigation/>
        </div>
    </div>
    <div class="page-body-card d-flex">
        <div class="container-xl">
            <slot/>
        </div>
    </div>
</div>
