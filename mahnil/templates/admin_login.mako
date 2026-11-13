<%inherit file="admin_master.mako" />
<%block name="title">Admin sign in — Mahnil Digital</%block>

<main class="mx-auto flex min-h-screen max-w-xl flex-col justify-center px-5 py-16">
  <a class="mb-10 w-fit text-sm text-slate-600 hover:text-slate-900" href="/">← Back to the website</a>
  <p class="mb-4 text-xs font-medium uppercase tracking-[0.18em] text-slate-600">Private workspace</p>
  <h1 class="text-4xl font-light tracking-tight sm:text-5xl">Admin sign in</h1>
  <p class="mt-4 max-w-md text-base leading-7 text-slate-600">Sign in to edit the homepage, services, selected work, and free resources.</p>

  % if error:
    <p class="mt-6 rounded-sm border border-slate-200 bg-white px-4 py-3 text-sm" role="alert">${error | h}</p>
  % endif

  % if configured:
    <form action="/admin/login" method="post" class="mt-8 space-y-5 border border-slate-200 bg-white p-6 sm:p-8">
      <div>
        <label class="mb-2 block text-sm font-medium" for="username">Username</label>
        <input class="min-h-12 w-full border border-slate-200 bg-white px-4 py-3 text-base text-slate-900 outline-none focus:border-teal-700" id="username" name="username" autocomplete="username" required maxlength="128">
      </div>
      <div>
        <label class="mb-2 block text-sm font-medium" for="password">Password</label>
        <input class="min-h-12 w-full border border-slate-200 bg-white px-4 py-3 text-base text-slate-900 outline-none focus:border-teal-700" id="password" name="password" type="password" autocomplete="current-password" required maxlength="1024">
      </div>
      <button class="min-h-12 w-full bg-color-3 px-6 py-3 text-sm font-medium text-white hover:bg-teal-800" type="submit">Sign in</button>
    </form>
  % else:
    <p class="mt-8 border border-slate-200 bg-white px-5 py-4 text-sm leading-6 text-slate-600">Admin access is disabled until <code class="text-slate-900">YHTTP_ADMIN_USERNAME</code> and <code class="text-slate-900">YHTTP_ADMIN_PASSWORD</code> are configured.</p>
  % endif
</main>
