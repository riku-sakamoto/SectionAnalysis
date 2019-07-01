
var LicenseFee=[
    {FeePerMin:100,Date:"2018/12/10",OwnedLicense:0}
];

var UseLicenseFee=[
    {SumFeeForDay:0},
    {SumFeeForMonth:0},
    {SumFeeForYear:0}
];

var grid_license_fee=document.getElementById("grid_license_fee");

var table_license_fee = new Handsontable(grid_license_fee,{
    data:LicenseFee,
    columns:[
        {
            type:"numeric",
            data:"FeePerMin"
        },
        {
            type:"text",
            data:"Date"
        },
        {
            type:"numeric",
            data:"OwnedLicense"
        }
    ],
    colHeaders:["ライセンス料(/分)","日付（年/月/日）","購入ライセンス数"]
});


document.getElementById('calc_start').addEventListener('click',
    function () {
        var hostUrl = 'http://localhost:8080/post';
        $.ajax({
            url: hostUrl,
            type: 'POST',
            dataType: 'json',
            data: JSON.stringify(LicenseFee[0]),
            contentType: 'application/json',
            timeout: 10000,
        }).done(function (data) {
            console.log("done");
            UseLicenseFee.SumFeeForDay=data["sum_fee_for_day"];
            UseLicenseFee.SumFeeForMonth=data["sum_fee_for_month"];
            UseLicenseFee.SumFeeForYear=data["sum_fee_for_year"];
            //もっとうまい方法があるはず
            //なぜかjinjia２の機能が動かない
            var target = document.getElementById("license_plot")
            target.innerHTML="<img src="+data["image_path"]+"/>"
            var target2 = document.getElementById("show_sum_fee_for_day");
            target2.innerHTML = '<font size="10">ライセンス使用料（/日）：'+UseLicenseFee.SumFeeForDay+"円</font>";
            var target3 = document.getElementById("show_sum_fee_for_month");
            target3.innerHTML = '<font size="10">ライセンス使用料（/月）：'+UseLicenseFee.SumFeeForMonth+"円</font>";
            var target4 = document.getElementById("show_sum_fee_for_year");
            target4.innerHTML = '<font size="10">ライセンス使用料（/年）：'+UseLicenseFee.SumFeeForYear+"円</font>";
        }).fail(function (XMLHttpRequest, textStatus, errorThrown) {
            console.log("failed");
        })
    });


