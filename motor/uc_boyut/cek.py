from playwright.sync_api import sync_playwright
import http.server, threading, functools
srv=http.server.ThreadingHTTPServer(('127.0.0.1',8765),functools.partial(http.server.SimpleHTTPRequestHandler,directory='/tmp/three'))
threading.Thread(target=srv.serve_forever,daemon=True).start()
with sync_playwright() as p:
    b=p.chromium.launch(args=['--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader','--ignore-gpu-blocklist'])
    pg=b.new_page(viewport={'width':980,'height':820}); err=[]
    pg.on('console',lambda m: err.append(m.text) if m.type in ('error','warning') else None); pg.on('pageerror',lambda e: err.append(str(e)))
    pg.goto('http://127.0.0.1:8765/kazan.html'); pg.wait_for_function('window.HAZIR===true',timeout=60000)
    pg.locator('canvas').screenshot(path='/tmp/three/kazan3d.png',omit_background=True)
    print('hata',err[:5]); b.close()
srv.shutdown()
