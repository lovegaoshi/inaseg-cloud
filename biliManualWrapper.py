import subprocess
if __name__ == '__main__':
    k = ['https://www.bilibili.com/video/BV1GY411M7ih', 'https://www.bilibili.com/video/BV1d34y1j7Jh', 'https://www.bilibili.com/video/BV1e3411V7EF', 'https://www.bilibili.com/video/BV1Br4y1473K', 'https://www.bilibili.com/video/BV1VF411j7XP', 'https://www.bilibili.com/video/BV19Y4y1r78v', 'https://www.bilibili.com/video/BV1Mr4y1b7H3', 'https://www.bilibili.com/video/BV1WA4y1S7o1', 'https://www.bilibili.com/video/BV1ES4y1b7ZD', 'https://www.bilibili.com/video/BV1YY4y1b7G7', 'https://www.bilibili.com/video/BV1ju411r7TK', 'https://www.bilibili.com/video/BV1R34y187j3', 'https://www.bilibili.com/video/BV1qv4y1K7mF', 'https://www.bilibili.com/video/BV1pr4y187pC', 'https://www.bilibili.com/video/BV1Yu411y7iD', 'https://www.bilibili.com/video/BV1zi4y1S7DZ', 'https://www.bilibili.com/video/BV1144y1P7x2', 'https://www.bilibili.com/video/BV1Hq4y1e7ex', 'https://www.bilibili.com/video/BV1JZ4y1z7VB', 'https://www.bilibili.com/video/BV13Y411H7em', 'https://www.bilibili.com/video/BV1JT4y1i78P', 'https://www.bilibili.com/video/BV1yP4y1T7DZ', 'https://www.bilibili.com/video/BV1pS4y1u7Xe', 'https://www.bilibili.com/video/BV1oa411b7Hb', 'https://www.bilibili.com/video/BV1hR4y1G7JL', 'https://www.bilibili.com/video/BV18u411Q74n', 'https://www.bilibili.com/video/BV1uq4y147nM', 'https://www.bilibili.com/video/BV15L411N7ZK', 'https://www.bilibili.com/video/BV1JF411E7Gb', 'https://www.bilibili.com/video/BV1jY411L7dH', 'https://www.bilibili.com/video/BV1Au41117vq', 'https://www.bilibili.com/video/BV1RT4y117jq', 'https://www.bilibili.com/video/BV1tb4y1H7vL', 'https://www.bilibili.com/video/BV1sa411q7gB', 'https://www.bilibili.com/video/BV1gm4y1D7dv', 'https://www.bilibili.com/video/BV1d34y1z75J', 'https://www.bilibili.com/video/BV1rm4y1Q7hw', 'https://www.bilibili.com/video/BV1Wi4y1R7js', 'https://www.bilibili.com/video/BV1fS4y1X7Xu', 'https://www.bilibili.com/video/BV1pq4y167Dk', 'https://www.bilibili.com/video/BV13P4y1L7G6', 'https://www.bilibili.com/video/BV1s44y1Y7YM', 'https://www.bilibili.com/video/BV1XS4y1d79e', 'https://www.bilibili.com/video/BV1WL4y1v7gM', 'https://www.bilibili.com/video/BV1sh411t77i', 'https://www.bilibili.com/video/BV1RS4y1R7uD', 'https://www.bilibili.com/video/BV1TT4y1d7Ui', 'https://www.bilibili.com/video/BV11u411d73Z', 'https://www.bilibili.com/video/BV1Sq4y197XZ', 'https://www.bilibili.com/video/BV1cu411f7vF', 'https://www.bilibili.com/video/BV1VL4y1B7mw', 'https://www.bilibili.com/video/BV1gL411G78t', 'https://www.bilibili.com/video/BV1644y1x7Nn', 'https://www.bilibili.com/video/BV1Dr4y127UX', 'https://www.bilibili.com/video/BV1BL4y1z7su', 'https://www.bilibili.com/video/BV1sv411g7C3', 'https://www.bilibili.com/video/BV1gq4y1N7fR', 'https://www.bilibili.com/video/BV1L34y1Q72S', 'https://www.bilibili.com/video/BV1Rf4y1V7WB', 'https://www.bilibili.com/video/BV1y3411z7Lu', 'https://www.bilibili.com/video/BV1Dq4y1X7br', 'https://www.bilibili.com/video/BV1cw411R73h', 'https://www.bilibili.com/video/BV1a64y1X7pm', 'https://www.bilibili.com/video/BV1h44y1276z', 'https://www.bilibili.com/video/BV1sU4y137J6', 'https://www.bilibili.com/video/BV1BM4y1M7Ac', 'https://www.bilibili.com/video/BV1pK4y1M7w1', 'https://www.bilibili.com/video/BV1ZX4y1c7rN', 'https://www.bilibili.com/video/BV1cg411376o', 'https://www.bilibili.com/video/BV19q4y1L7uE', 'https://www.bilibili.com/video/BV1Wq4y1s7k4', 'https://www.bilibili.com/video/BV1ZX4y1A7sQ', 'https://www.bilibili.com/video/BV1tf4y1t7yQ', 'https://www.bilibili.com/video/BV1Ub4y1d7mF', 'https://www.bilibili.com/video/BV18K4y1u78F', 'https://www.bilibili.com/video/BV1V44y1B7AN', 'https://www.bilibili.com/video/BV1FQ4y1R7jL', 'https://www.bilibili.com/video/BV1xQ4y197Tt', 'https://www.bilibili.com/video/BV1eK4y137fQ', 'https://www.bilibili.com/video/BV1154y137Tq', 'https://www.bilibili.com/video/BV1FK4y137dp', 'https://www.bilibili.com/video/BV1mK4y1G7gL', 'https://www.bilibili.com/video/BV1KA41137sR', 'https://www.bilibili.com/video/BV1jB4y1u7hL']
    #print(watch())
    for i in k:
        print('calling biliupWrapper on', i)
        p = subprocess.Popen(['python', 'biliupWrapper.py', '--media='+i])
        p.wait()