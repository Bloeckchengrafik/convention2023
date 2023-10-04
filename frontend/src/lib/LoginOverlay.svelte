<script lang="ts">
    import {Stack, LockKey} from "phosphor-svelte";
    import {endpoint} from "$lib/api";
    import {poll} from "$lib/poll";
    import {fade} from 'svelte/transition';

    type AuthData = {
        ok: boolean,
        error: string,
    }

    let auth_data: AuthData = {
        ok: true,
        error: "",
    }

    let timeout: any = null
    let should_disappear = true

    poll(async () => {
        let awaited = await endpoint<AuthData>(`auth/is_authenticated`)
        auth_data = awaited

        if (awaited.ok) {
            timeout = setTimeout(() => {
                should_disappear = true
            }, 1000)
        } else {
            if (timeout) clearTimeout(timeout)
            should_disappear = false
        }
    }, 100);
</script>

{#if !should_disappear}
    <div style="position: absolute; top: 0; left: 0; right: 0; bottom: 0; backdrop-filter: brightness(0.5) blur(3px);z-index: 999999;display: flex; flex-direction: column; justify-content: center;align-items: center"
         transition:fade>
        <div class="card">
            <div class="card-header">
                <Stack size="32"/>
                <h1>
                    <span class="text-primary">3D</span>Cut
                </h1>
            </div>
            <div class="card-body d-flex flex-column justify-content-center align-items-center p-5">
                <LockKey size="128"/>
                <h1>Console locked</h1>
                <p>We'll be back soon</p>
                <br/>
                <span class="text-muted">
                    {#if auth_data.error}
                        {auth_data.error}
                    {:else}
                        Please wait...
                    {/if}
                </span>
            </div>
        </div>
    </div>
{/if}
