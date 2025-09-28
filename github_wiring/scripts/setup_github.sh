#!/usr/bin/env bash
# Requires: gh CLI logged in to GitHub as troymork; git; node (for site later)
set -e

USER="troymork"

# Create repos if they don't exist
gh repo view $USER/solvency-automation >/dev/null 2>&1 || gh repo create $USER/solvency-automation --private -y
gh repo view $USER/solvency-site >/dev/null 2>&1 || gh repo create $USER/solvency-site --public -y

echo "Repos ensured."

# Initialize solvency-automation repo
TMP=$(mktemp -d)
mkdir -p "$TMP/solvency-automation"
cp -r ../n8n_flows ../prompts ../certificate ../ffmpeg_templates ../notion "$TMP/solvency-automation/"
cat > "$TMP/solvency-automation/README.md" <<'MD'
# Solvency Automation
n8n flows… agent prompts… templates… and Notion CSVs for the Solvency initiative.
MD
cd "$TMP/solvency-automation"
git init
git add .
git commit -m "Initial commit: flows, prompts, templates, notion CSVs"
git branch -M main
git remote add origin "https://github.com/$USER/solvency-automation.git"
git push -u origin main
cd -

# Initialize solvency-site repo
mkdir -p "$TMP/solvency-site"
cp -r ../next_content_schema "$TMP/solvency-site/content"
mkdir -p "$TMP/solvency-site/.github/workflows"
cat > "$TMP/solvency-site/.github/workflows/deploy.yml" <<'YML'
name: Deploy static site
on:
  push:
    branches: [ "main" ]
permissions:
  contents: read
  pages: write
  id-token: write
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
      - run: npm ci
      - run: npm run build
      - run: npm run export
      - uses: actions/upload-pages-artifact@v3
        with:
          path: out
  deploy:
    needs: build
    runs-on: ubuntu-latest
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    steps:
      - id: deployment
        uses: actions/deploy-pages@v4
YML

# Minimal Next.js static site
cat > "$TMP/solvency-site/package.json" <<'JSON'
{
  "name": "solvency-site",
  "version": "0.1.0",
  "private": true,
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "export": "next export",
    "start": "next start"
  },
  "dependencies": {
    "next": "14.2.5",
    "react": "18.2.0",
    "react-dom": "18.2.0"
  }
}
JSON

cat > "$TMP/solvency-site/next.config.js" <<'JS'
/** @type {import('next').NextConfig} */
const isGH = process.env.GITHUB_ACTIONS === 'true';
const repo = 'solvency-site';
module.exports = {
  output: 'export',
  images: { unoptimized: true },
  assetPrefix: isGH ? `/${repo}/` : undefined,
  basePath: isGH ? `/${repo}` : undefined
};
JS

mkdir -p "$TMP/solvency-site/pages"
cat > "$TMP/solvency-site/pages/_app.js" <<'JS'
import '../styles.css'
export default function App({ Component, pageProps }) { return <Component {...pageProps} /> }
JS

cat > "$TMP/solvency-site/pages/index.js" <<'JS'
import Link from 'next/link'
export async function getStaticProps(){ 
  const res = await import('../content/explainer.json')
  return { props: { explainer: res.default } }
}
export default function Home({ explainer }){
  return (
    <main style={{maxWidth:900,margin:'40px auto',padding:'0 16px'}}>
      <h1>{explainer.title}</h1>
      <p>{explainer.hero?.headline}</p>
      <ul>
        <li><Link href="/explainer">Explainer</Link></li>
        <li><Link href="/one-pager">One Pager</Link></li>
        <li><Link href="/infographics">Infographics</Link></li>
        <li><Link href="/social-kit">Social Kit</Link></li>
      </ul>
    </main>
  )
}
JS

cat > "$TMP/solvency-site/pages/explainer.js" <<'JS'
export async function getStaticProps(){ const res = await import('../content/explainer.json'); return { props: { data: res.default } } }
export default function Page({ data }){
  return <main style={{maxWidth:900,margin:'40px auto',padding:'0 16px'}}>
    <h1>{data.title}</h1>
    {data.sections?.map((s,i)=> <section key={i}><h2>{s.heading}</h2><p>{s.copy}</p>{s.bullets && <ul>{s.bullets.map((b,bi)=><li key={bi}>{b}</li>)}</ul>}</section>)}
  </main>
}
JS

cat > "$TMP/solvency-site/pages/one-pager.js" <<'JS'
export async function getStaticProps(){ const res = await import('../content/one_pager.json'); return { props: { data: res.default } } }
export default function Page({ data }){
  return <main style={{maxWidth:900,margin:'40px auto',padding:'0 16px'}}>
    <h1>{data.title}</h1>
    {data.blocks?.map((b,i)=> <div key={i}><strong>{b.type}</strong><div>{b.text||b.label}</div></div>)}
  </main>
}
JS

cat > "$TMP/solvency-site/pages/infographics.js" <<'JS'
export async function getStaticProps(){ const res = await import('../content/infographics_hub.json'); return { props: { data: res.default } } }
export default function Page({ data }){
  return <main style={{maxWidth:900,margin:'40px auto',padding:'0 16px'}}>
    <h1>{data.title}</h1>
    <ul>{data.figures?.map(f=><li key={f.id}>{f.title}</li>)}</ul>
  </main>
}
JS

cat > "$TMP/solvency-site/pages/social-kit.js" <<'JS'
export async function getStaticProps(){ const res = await import('../content/social_kit.json'); return { props: { data: res.default } } }
export default function Page({ data }){
  return <main style={{maxWidth:900,margin:'40px auto',padding:'0 16px'}}>
    <h1>{data.title}</h1>
    {data.posts?.map((p,i)=> <article key={i}><h3>{p.platform}</h3><p>{p.copy}</p></article>)}
  </main>
}
JS

cat > "$TMP/solvency-site/styles.css" <<'CSS'
*{box-sizing:border-box} body{font-family:ui-sans-serif,system-ui,Arial,Helvetica,sans-serif;line-height:1.5}
h1,h2,h3{line-height:1.2}
CSS

cat > "$TMP/solvency-site/README.md" <<'MD'
# Solvency Site
Static-export Next.js site. Content lives in `/content` as JSON generated by your agents.

## Local
npm ci
npm run dev

## Deploy
Push to main… GitHub Pages action builds and deploys automatically.
MD

cd "$TMP/solvency-site"
git init
git add .
git commit -m "Initial commit: static Next scaffold + content"
git branch -M main
git remote add origin "https://github.com/$USER/solvency-site.git"
git push -u origin main
cd -

echo "✅ Repos pushed. Enable GitHub Pages for solvency-site → Settings → Pages → Source: GitHub Actions."


# Create and push solvency-agents
gh repo view $USER/solvency-agents >/dev/null 2>&1 || gh repo create $USER/solvency-agents --public -y
AGTMP=$(mktemp -d)
mkdir -p "$AGTMP/solvency-agents"
cp -r ../solvency-agents/* "$AGTMP/solvency-agents/"
cd "$AGTMP/solvency-agents"
git init
git add .
git commit -m "Initial commit: multiplexed FastAPI agent and GHCR workflow"
git branch -M main
git remote add origin "https://github.com/$USER/solvency-agents.git"
git push -u origin main
cd -

echo "✅ Agents repo pushed. Once Actions build completes, run docker compose up in github_wiring/compose."
