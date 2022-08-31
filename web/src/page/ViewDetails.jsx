import React from 'react'

const ViewDetails = (props) => {

  const { filterData } = props
  const styleTd = { width: 200, overflow: "hidden", whiteSpace: "nowrap", padding: "5px 5px" }


  return (
    <div style={{ width: '100%' }}>
      <table border="1" style={{
        borderCollapse: "collapse",
        borderColor: "#DDD", backgroundColor: "#FFFFFF"
      }}>
        <thead>
          <tr style={{ backgroundColor: '#FFF', color: "#AAA" }}>
            <th>date</th>
            <th>Name</th>
            <th>type</th>
          </tr>
        </thead>
        <tbody>
          {filterData.map((row, idx) => (
            <tr key={idx}>

              <td style={styleTd}>{row.date}</td>
              <td style={styleTd}>{row.Name}</td>
              <td style={styleTd}>{row.status}</td>

            </tr>
          ))}
        </tbody>
      </table>

    </div>
  )
}

export default ViewDetails