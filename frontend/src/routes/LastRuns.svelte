<script lang="ts">
    import {endpoint} from "$lib/api";
    import type {Pipeline} from "$lib/endpoints";
    import Pipelines from "./Pipelines.svelte";
    import {poll} from "$lib/poll";

    let data = endpoint<Pipeline[]>("pipeline")

    poll(async () => {
        let awaited = await endpoint<Pipeline[]>("pipeline")
        data = Promise.resolve(awaited)
    }, 5000)
</script>

{#await data}
    <div class="h-full d-flex justify-content-center align-items-center">
        <span class="status status-orange">Loading</span>
    </div>
{:then pipelines}
    <Pipelines {pipelines}/>
{:catch error}
    <div class="h-full d-flex justify-content-center align-items-center">
        <span class="status status-red">Error: {error}</span>
    </div>
{/await}
