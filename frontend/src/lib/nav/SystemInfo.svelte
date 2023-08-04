<script lang="ts">
    import {poll} from "$lib/poll";
    import {endpoint} from "$lib/api";
    import {ChatCircleDots, Clock, GitBranch} from "phosphor-svelte";
    import type {IndexEndpoint} from "$lib/endpoints";

    let result: IndexEndpoint | null = null
    let lastUpdate = Date.UTC(0, 0)
    let neededUpdate = Date.now() - 700
    let wasOffline = true

    poll(async () => {
        result = await endpoint<IndexEndpoint>("")
        lastUpdate = Date.now()
    }, 500);

    poll(async () => {
        neededUpdate = Date.now() - 700
        if (neededUpdate < lastUpdate) {
            if (wasOffline) {
                wasOffline = false
                console.log("We're Online, yay!")
            }
        } else {
            if (!wasOffline) {
                wasOffline = true
                console.log("We're Offline, is the server restarting?")
            }
        }
    }, 250);
</script>

{#if result}
    <span class="d-flex justify-content-center gap-2"><ChatCircleDots size="20"/>{result.message}</span>
    <span class="d-flex justify-content-center gap-2"><Clock size="20"/>{result.server_time}</span>
    <span class="d-flex justify-content-center gap-2"><GitBranch size="20"/>{result.version}#{result.git_commit_hash}</span>
    {#if neededUpdate < lastUpdate}
        <span class="status status-green">Online</span>
    {:else}
        <span class="status status-red">Offline</span>
    {/if}
{:else}
    <span class="status status-orange">Unknown</span>
{/if}
