<script lang="ts">
    import {poll} from "$lib/poll";
    import {endpoint} from "$lib/api";
    import {ChatCircleDots, Clock, GitBranch} from "phosphor-svelte";
    import type {IndexEndpoint} from "$lib/endpoints";

    let result: IndexEndpoint | null = null
    let lastUpdate = Date.UTC(0, 0)
    let neededUpdate = Date.now() - 1000
    let wasOffline = true

    poll(async () => {
        result = await endpoint<IndexEndpoint>("")
        lastUpdate = Date.now()
    }, 500);

    poll(async () => {
        neededUpdate = Date.now() - 1000
        if (neededUpdate < lastUpdate) {
            if (wasOffline) {
                wasOffline = false
                console.log("We're online, yay!")
            }
        } else {
            if (!wasOffline) {
                wasOffline = true
                console.log("We're offline, is the server restarting?")
            }
        }
    }, 250);
</script>

{#if result}
    <span class="d-flex justify-content-center gap-2"><ChatCircleDots size="20"/>{result.message}</span>
    <span class="d-flex justify-content-center gap-2"><Clock size="20"/>{result.server_time}</span>
    <span class="d-flex justify-content-center gap-2"><GitBranch size="20"/>{result.version}#{result.git_commit_hash}</span>
    {#if neededUpdate < lastUpdate}
        <span class="status status-green"><span class="status-dot status-dot-animated"></span>Online</span>
    {:else}
        <span class="status status-red"><span class="status-dot"></span>Offline</span>
    {/if}
{:else}
    <span class="status status-orange"><span class="status-dot"></span>Unknown</span>
{/if}
