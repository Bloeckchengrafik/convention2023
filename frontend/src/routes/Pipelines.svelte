<script lang="ts">
    import type {Pipeline} from "$lib/endpoints";
    import Empty from "$lib/Empty.svelte";
    import {
        IdentificationCard,
        CalendarBlank,
        PlayPause,
        Flag,
        Cpu,
        Clock,
        X,
        Scissors,
        CheckCircle,
        Warning,
        EggCrack
    } from "phosphor-svelte";
    import {endpoint} from "$lib/api";

    export let pipelines: Pipeline[]

    let statusColors = {
        "pending": "indigo",
        "processable": "purple",
        "processing": "orange",
        "cutting": "cyan",
        "done": "lime",
        "error": "red"
    }

    let statusIcons = {
        "pending": PlayPause,
        "processable": Clock,
        "processing": Cpu,
        "cutting": Scissors,
        "done": CheckCircle,
        "error": Warning,
        "BUILDING": EggCrack
    }
</script>

{#if pipelines.length > 0}
    {#each pipelines as pipeline}
        <div class="card p-2 px-3 mb-2">
            <h3 class="fw-normal m-0 d-flex gap-4">
                <span><IdentificationCard size="23"/> ID <b style="width: 10ch;display: inline-block">#{pipeline.id}</b></span>
                <span><CalendarBlank size="23"/> TIME <b>{pipeline.timestamp}</b></span>
                <a href="/" on:click|preventDefault={() => {
                    endpoint(`pipeline/id/${pipeline.id}/complete_early`)
                }}><Flag size="23"/></a>
                <a href="/" on:click|preventDefault={() => {
                    endpoint(`pipeline/id/${pipeline.id}/cancel`)
                }}><X size="23"/></a>
            </h3>
            <span class="ribbon w-150 bg-{statusColors[pipeline.status]} d-flex justify-content-start gap-2"><svelte:component this={statusIcons[pipeline.status]}
                                                                                     size="23"/> {pipeline.status}</span>
        </div>
    {/each}
{:else}
    <Empty></Empty>
{/if}

<style>
    .w-150 {
        width: 150px;
        text-align: left;
    }
</style>