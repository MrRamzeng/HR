function getResults(json) {
  let results = JSON.parse(json.textContent)
  return results.length ? results : [{'timer': 30, 'empty': true}]
}

let results30 = getResults(document.getElementById('json_results_30'))
let results60 = getResults(document.getElementById('json_results_60'))
let results120 = getResults(document.getElementById('json_results_120'))
const container = document.getElementById('results')
const root = ReactDOM.createRoot(container)

if (!isAuth) {
  function sort_result(results, result) {
    results.push(result)
    results.sort((a, b) => (
        a['max_score'] * a['best_accuracy'] / a['max_speed'] <=
        b['max_score'] * b['best_accuracy'] / b['max_speed']
      ) ? 1 : -1
    )

    if (results.length > 10) {
      const last = results[results.length - 1]
      last['unregister'] ? results.splice(9, 1) : results.splice(9)
    }
    return results
  }

  const aResult = JSON.parse(localStorage.getItem('anonym_result'))
  if (aResult['timer'] === '30') {
    results30 = sort_result(results30, aResult)
  } else if (aResult['timer'] === '60') {
    results60 = sort_result(results60, aResult)
  } else {
    results120 = sort_result(results120, aResult)
  }
}

root.render(
  <>
    <Table results={results30}/>
    <Table results={results60}/>
    <Table results={results120}/>
  </>
)

const TableHeader = ({data, colSpan}) => {
  return (
    <th colSpan={colSpan}
      className="px-6 py-3 text-center font-medium text-gray-900 whitespace-nowrap dark:text-white"
    >{data}</th>
  )
}

const TableData = ({data, colSpan}) => {
  return (<td colSpan={colSpan} className="px-6 py-3 text-center">{data}</td>)
}

const TableRow = ({classes, children}) => {
  return (
    <tr className={`border-b dark:border-gray-700 ${classes}`}>{children}</tr>
  )
}

function Table({results = []}) {
  const username = `{{ request.user.username }}`
  return (
    <table className="w-1/3 mx-1 text-gray-500 text-sm text-left dark:text-gray-400">
      <thead
        className="text-xs text-gray-700 uppercase bg-gray-50 dark:bg-gray-700 dark:text-gray-400"
      >
      <tr><TableHeader data={`${results[0]['timer']} секунд`} colSpan="5"/></tr>

      <tr>
        <th scope="col" className="px-6 py-4">Место</th>
        <th scope="col" className="px-6 py-4">Пользователь</th>
        <th scope="col" className="px-6 py-4">Счет</th>
        <th scope="col" className="px-6 py-4">Скорость</th>
        <th scope="col" className="px-6 py-4">Аккуратность</th>
      </tr>
      </thead>
      <tbody id={`${results[0]['timer']}s`}>
      {results[0]['empty'] ?
        <TableRow>
          <TableData data="Пока нет результатов" colSpan="5"/>
        </TableRow>
        : results.length === 2 && results[1]['empty'] ?
        <TableRow>
          <TableHeader data='1'/>
          <TableData data={results[0]['user__username']}/>
          <TableData data={results[0]['max_score']}/>
          <TableData data={results[0]['max_speed']}/>
          <TableData data={`${results[0]['best_accuracy']}%`}/>
        </TableRow>
        :
        <>
          {results.map((result, position) => (
            <TableRow
              key={result['timer'] + position}
              classes={
                `${
                  username === result['user__username'] || result['unregister'] ?
                  "bg-gray-50 dark:bg-gray-900" : "bg-white dark:bg-gray-800"
                }`
              }
            >
              <TableHeader data={result['unregister'] ? '' : result['position'] || position + 1}/>
              {username === result['user__username'] || result['unregister'] ?
                <>
                  <TableHeader data={result['user__username']}/>
                  <TableHeader data={result['max_score']}/>
                  <TableHeader data={result['max_speed']}/>
                  <TableHeader data={`${result['best_accuracy']}%`}/>
                </>
              :
                <>
                  <TableData data={result['user__username']}/>
                  <TableData data={result['max_score']}/>
                  <TableData data={result['max_speed']}/>
                  <TableData data={`${result['best_accuracy']}%`}/>
                </>
              }
            </TableRow>
          ))}
        </>
      }
      </tbody>
    </table>
  )
}