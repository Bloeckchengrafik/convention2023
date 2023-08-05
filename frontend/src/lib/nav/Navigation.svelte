<script lang="ts">
    import {Stack} from "phosphor-svelte";
    import SystemInfo from "$lib/nav/SystemInfo.svelte";
</script>

<div class="d-flex flex-row justify-content-between align-items-center">
    <a class="d-flex flex-row gap-3 text-white text-decoration-none" href="/">
        <Stack size="32"/>
        <h1>
            <span class="text-primary">3D</span>Cut
        </h1>
    </a>
    <div class="d-flex flex-row gap-3 justify-content-center align-items-center h-full">
        <SystemInfo/>
    </div>
</div>
