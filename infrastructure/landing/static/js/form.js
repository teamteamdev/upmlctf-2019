document.addEventListener('DOMContentLoaded', () => {

    const $ = (id) => document.getElementById(id) // This is not jQuery, sorry, not this time

    let p

    const toggle = (ids, cls = 'on') =>
        ids.forEach(id => $(id).classList.toggle(cls))

    const count = (to) => {
        const now = new Date().getTime()
        d = to - now
        $('timer').innerHTML = (Math.floor(d / (1000 * 60 * 60 * 24)) * 24 + Math.floor((d % (1000 * 60 * 60)) / (1000 * 60 * 60))) + ':' + Math.floor((d % (1000 * 60 * 60)) / (1000 * 60)) + ':' + Math.floor((d % (1000 * 60)) / 1000)
    }

    const switchPlans = () => {
        toggle(['plan3', 'plan2'], 'plan--chosen')
        p = document.querySelector('.plan--chosen').dataset.p
    }

    $('open').onclick = () => {
        toggle(['modal', 'mw', 'step1'])

        $('plan2').classList.add('on')
        $('plan3').classList.add('on')

        $('plan2').onclick = switchPlans
        $('plan3').onclick = switchPlans

        $('next').onclick = () => {
            const data = new FormData()
            data.append('token', `${~~(Date.now() / 1000)}.${p || 3}`)

            const rq = new XMLHttpRequest()
            rq.open('POST', window.location.href + 'api/apply', true)
            rq.onload = () => {
                re = JSON.parse(rq.responseText)
                a = re.active_on
                t = re.token
                if ('name' in re) {
                    document.querySelector('.plan--chosen .plan__name').innerHTML = re.name
                }
                name = $('name').value
                $('title').innerHTML = (name ? `${name}, ` : '') + 'Ваша заявка оформлена'
                toggle(['step1', 'step2'])

                document.querySelector('.plan:not(.plan--chosen)')
                    .classList.toggle('on')

                $('plan2').onclick = undefined
                $('plan3').onclick = undefined

                $('closeText').innerHTML = 'Пожалуйста, не закрывайте это окно. Душно'

                $('next').onclick = () => {
                    toggle(['modal', 'step2', 'mw'])
                }

                $('next').innerHTML = 'Закрыть'
                count(a * 1000)
                inter = setInterval(() => {
                    if ((a * 1000) - Date.now() < 0) {
                        $('timer').innerHTML = t
                        $('timerText').innerHTML = 'Ваш токен для <a href="tg://resolve?domain=bank_bank_bot">телеграм-бота</a>'
                        $('closeText').innerHTML = 'Закройте окно, ДУЕТ'
                        clearInterval(inter)
                    } else {
                        count(a * 1000)
                    }
                }, 100)
            }
            rq.send(data)
        }
    }

})
