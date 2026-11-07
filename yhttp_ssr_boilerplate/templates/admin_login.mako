<%inherit file="admin_master.mako" />
<%block name="title">Admin sign in — [Agency Name]</%block>

<main class="mx-auto flex min-h-screen max-w-xl flex-col justify-center px-5 py-16">
  <a class="mb-10 w-fit text-sm text-color-2 hover:text-color-4" href="/">← Back to the website</a>
  <p class="mb-4 text-xs font-medium uppercase tracking-[0.18em] text-color-2">Private workspace</p>
  <h1 class="text-4xl font-light tracking-tight sm:text-5xl">Admin sign in</h1>
  <p class="mt-4 max-w-md text-base leading-7 text-color-2">Sign in to edit the homepage, services, selected work, and free resources.</p>

  % if error:
    <p class="mt-6 rounded-sm border border-color-4/30 bg-color-1 px-4 py-3 text-sm" role="alert">${error | h}</p>
  % endif

  % if configured:
    <form action="/admin/login" method="post" class="mt-8 space-y-5 border border-color-4/20 bg-color-1/70 p-6 sm:p-8">
      <div>
        <label class="mb-2 block text-sm font-medium" for="username">Username</label>
        <input class="min-h-12 w-full border border-color-2/45 bg-color-5 px-4 py-3 text-base text-color-4 outline-none focus:border-color-4" id="username" name="username" autocomplete="username" required maxlength="128">
      </div>
      <div>
        <label class="mb-2 block text-sm font-medium" for="password">Password</label>
        <input class="min-h-12 w-full border border-color-2/45 bg-color-5 px-4 py-3 text-base text-color-4 outline-none focus:border-color-4" id="password" name="password" type="password" autocomplete="current-password" required maxlength="1024">
      </div>
      <button class="min-h-12 w-full bg-color-4 px-6 py-3 text-sm font-medium text-color-5 hover:bg-color-4/90" type="submit">Sign in</button>
    </form>
  % else:
    <p class="mt-8 border border-color-4/20 bg-color-1/70 px-5 py-4 text-sm leading-6 text-color-2">Admin access is disabled until <code class="text-color-4">YHTTP_ADMIN_USERNAME</code> and <code class="text-color-4">YHTTP_ADMIN_PASSWORD</code> are configured.</p>
  % endif
</main>
