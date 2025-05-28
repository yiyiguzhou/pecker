<script type="text/javascript">
    var curLoopNum = 1
    var curActionNum = 0

    function filterTestcaseResult(id, value, index)
    {
        filterResult(id, value, index, true)
    }

    function filterLoopResult(id, value, index)
    {
        filterResult(id, value, index, false)
        var loopTable = document.getElementById(id);
        console.log(loopTable.rows.length)
        for(var i=1, rows = loopTable.rows.length; i < rows; i++)
        {
            if(loopTable.rows[i].style.display == "table-row")
            {
                filterTestcaseTable(loopTable.rows[i])
                return
            }
        }
        //全部隐藏，则表格全部清空
        filterTestcaseTable(loopTable.rows[0])
    }

    function filterResult(id, value, index, care_loop=false)
    {
        var mytable = document.getElementById(id);
        if(mytable == null)
        {
            alert("not found")
            return
        }
        for(var i=1, rows=mytable.rows.length; i < rows; i++)
        {
            if(mytable.rows[i].cells[0].innerHTML != curLoopNum && care_loop)
            {
                mytable.rows[i].style.display = 'none'
            }
            else if(value == "all")
            {
                mytable.rows[i].style.display = 'table-row'
            }
            else if(mytable.rows[i].cells[index].innerHTML.indexOf(value) != -1)
            {
                mytable.rows[i].style.display = 'table-row'
            }
            else
            {
                mytable.rows[i].style.display = 'none'
            }
        }
    }

    function filterTestcaseTable(e)
    {
        console.log(e)
        var loopNum = e.cells[0].innerHTML
        curLoopNum = loopNum

        //修改用例表格标题
        var testcaseHandle = document.getElementById("testcaseTitle")
        testcaseHandle.innerHTML = "第" + loopNum +"次用例执行汇总"

        var testcaseTable = document.getElementById('testcaseTable')
        for(var i=1, rows=testcaseTable.rows.length; i < rows; i++)
        {
            if(testcaseTable.rows[i].cells[0].innerHTML != loopNum)
            {
                testcaseTable.rows[i].style.display = 'none'
            }
            else
            {
                testcaseTable.rows[i].style.display = 'table-row'
            }
        }
        // 修改用例表结果选项为all
        document.getElementById('testcase_result').options[0].selected = true
    }

    function filterActionHttpTable(e)
    {
        console.log(e)
        var actionNum = e.cells[0].innerHTML
        curActionNum = actionNum

        //修改用例表格标题
//        var testcaseHandle = document.getElementById("testcaseTitle")
//        testcaseHandle.innerHTML = "第" + loopNum +"次用例执行汇总"

        var actionHttpTable = document.getElementById('pingbackActionHttpTable')
        for(var i=1, rows=actionHttpTable.rows.length; i < rows; i++)
        {
            if(actionHttpTable.rows[i].cells[0].innerHTML != actionNum)
            {
                actionHttpTable.rows[i].style.display = 'none'
            }
            else
            {
                actionHttpTable.rows[i].style.display = 'table-row'
            }
        }
        // 修改用例表结果选项为all
        document.getElementById('pingbackDetailAction').options[0].selected = true
    }

</script>