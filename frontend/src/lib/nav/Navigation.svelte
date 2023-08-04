<script lang="ts">
    import {Stack} from "phosphor-svelte";
    import SystemInfo from "$lib/nav/SystemInfo.svelte";
</script>

<div class="d-flex flex-row justify-content-between align-items-center">
    <div class="d-flex flex-row gap-3">
        <Stack size="32"/>
        <h1>3Scan</h1>
    </div>
    <div class="d-flex flex-row gap-3 justify-content-center align-items-center h-full">
        <SystemInfo/>
    </div>
</div>
